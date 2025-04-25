# mcs598-SEERCancerStudy
Replication of the Paper: Reproducible Survival Prediction with SEER Cancer Data

This repository contains code and results from replicating the experimental setup outlined in in _Reproducible Survival Prediction with SEER Cancer Data_ submitted to the Machine Learning for Healthcare 2018 conference. (https://proceedings.mlr.press/v85/hegselmann18a/hegselmann18a.pdf, https://proceedings.mlr.press/v85/hegselmann18a/hegselmann18a-supp.pdf)

<h1><ins>Repository Overview:</ins></h1>
- **/_results**: Files used to perform manual steps and analysis of experimental results. attribute_table.xlsx and feature_mapping_table.pdf were used in creating the feature map between the 2016 database and the 2023 database. hyperparameters.xlsx was used for analysis of the tuning models. results_final.xlsx was used for analysis of the final models.
- **/_results/FINAL_MODELS**: Raw experimental results for 24 final models and combined_results.csv file which contains all validation and testing results.
- **/_results/TUNING**: Raw experimental results for 2,570 tuning models. Each of the 12 top-level folders contains a combined_results.csv file with the validation results for that model and cancer type. Survival durations are combined.
- **/cohort_2025**: SEER*Stat session files to reproduce data selections and original data exports from SEER*Stat for each session file.
- **/data_breast**: Converted input data for breast cancer analysis.
- **/data_lung**: Converted input data for lung and bronchus cancer analysis.
- **/lib**: Python classes and functions used for the experiments.
- **main.py**: Main routine to perform the experiments.
- **requirements.txt**: Python dependencies (can be installed with pip, e.g. in a virtual environment).

<h1><ins>Additional Scripts:</ins></h1>
- **attribute_importance_graphs.py**: Script to analyze the relative importance of attributes in the final models. 
- **collect_cluster_results_csv.py**: Script to parse all validation and test results in a folder structure and write to a csv file.
- **feature_analysis.py**: Script to perform socioeconomic feature vs. survivability analysis.
- **model_tuner.py**: Script to run model tuning. The model which is tuned depends on the provided commandline arguments.
- **run_final_models.py**: Script to run all final models.
- **sas_matrix_formatter.py**: Script to convert SEER*Stat case listing data exports into experiment's input data format.

<h1><ins>Results Structure:</ins></h1>
- **/[date_time]_exeriment-0/arguments.txt**: Commandline arguments for main.py call.
- **/[date_time]_exeriment-0/results_importance.txt**: Relative importance of each attribute in experiment. Used in attribute importance analysis. Only present if "--importance" argument supplied. 
- **/[date_time]_exeriment-0/results_test.txt**: AUC, F1, and ACC for test dataset. Used in final model testing. Only present if "--test" argument supplied.
- **/[date_time]_exeriment-0/results_validate.txt**: AUC, F1, and ACC for validation dataset. Used in model tuning. 

<h1><ins>Execution Steps:</ins></h1>
1) **Access Source Code**: Download and unzip source code on PC.
2) **Setup Environment**: Ensure requirements listed in requirements.txt are met, installing with pip as needed. Python version: 3.10.11.
3) **Data Coversion**: Re-convert data if desired. 
		In commandline, run command below. Copy "INCIDENCES.txt", "CASES.csv", and "matrix_reformat.sas" in "\cohort_2025\data_Breast-noDetroit-allLA-ASCII_250406-1620" to "\data_breast".
```
$ python sas_matrix_formatter.py --matrix \cohort_2025\data_Breast-noDetroit-allLA-ASCII_250406-1620\matrix.txt --specs --matrix \cohort_2025\data_Breast-noDetroit-allLA-ASCII_250406-1620\matrix.sas
```
		In commandline, run command below. Copy "INCIDENCES.txt", "CASES.csv", and "matrix_reformat.sas" in "\cohort_2025\data_Lung-noDetroit-allLA-ASCII_250411-0923" to "\data_lung".
```
$ python sas_matrix_formatter.py --matrix \cohort_2025\data_Lung-noDetroit-allLA-ASCII_250411-0923\matrix.txt --specs --matrix \cohort_2025\data_Lung-noDetroit-allLA-ASCII_250411-0923\matrix.sas
```
4) **Model Tuning**: Re-tune models if desired. In commandline, run command below. 
		WARNING: Can be very time consuming. See report for runtime analysis.
```
$ python model_tuner.py --type 2 --task 12 --data breast
```
Commandline Arguments:
  "--type", 
	2 = Logistic Regression (LOG REG), 13 combinations ~5 minutes
	3 = Logistic Regression with 1-N Encoding (LOG REG 1-N ENC), 13 combinations ~10 minutes
	4 = Multilayer Perceptron (MLP), 288 combinations ~30 hours
	5 = Multilayer Perceptron with 1-N Encoding (MLP 1-N ENC), 288 combinations ~36 hours
	6 = Embedded Multilayer Perceptron (MLPEmb 1-N ENC), 36 or 54 combinations ~9 or ~13 hours
  "--task",
	12 = 1-yr survival prediction
	60 = 5-yr survival prediction
  "--data"
	breast = breast cancer data
	lung = lung and bronchus data
5) **Analyze Tuning Results**: Combine all validation results and review csv. In commandline, run command below. Open combined_results.csv. Sort by folder, model, survial duration, then auc+f1 to determine best model for each model/cancer type/survial duration. The best hyperparameters should be entered into run_final_models.py.
```
$ python collect_cluster_results_csv.py \TUNING
```
6) **Final Model Execution**: Run final models using best tuning parameters. In commandline, run command below. WARNING: 24 models ~2 hours
```
$ python run_final_models.py
```
7) **Analyze Final Model Results**: Combine all testing results and review csv. In commandline, run command below. Open combined_results.csv to review test results.
```
$ python collect_cluster_results_csv.py \FINAL_MODELS
```
8) **Attribute Importance Analysis**: Review the top 10 attributes ranked on the sum of relative importance over all models. In commandline, run command below. Four graphs will be displayed, one for each cancer type/survival duration. Top 10 attribute lists will be printed to the console.
```
$ python attribute_importance_graphs.py
```
9) **Perform Socioeconomic Feature Analysis**: Analyze the impact of socioeconomic features on cancer survivability.
		To analyze the impact on breast cancer, run command below in commandline. Two graphs will be displayed, one for each socioeconomic feature.
```
$ python feature_analysis.py --spec data_breast/matrix_reformat.sas --data data_breast/INCIDENCES.txt"
```
		To analyze the impact on lung and bronchus cancer, run command below in commandline. Two graphs will be displayed, one for each socioeconomic feature.
```
$ python feature_analysis.py --spec data_lung/matrix_reformat.sas --data data_lung/INCIDENCES.txt"
```

<h1><ins>Additional Functionality</ins></h1>
Additonal functionality, which was not used for replication of the paper, is available by directly calling the main.py script. 
Run the command below with commandline argument "-h" to get an overview of all command line arguments, including SVM models and survival regression.
```
$ python main.py -h
```