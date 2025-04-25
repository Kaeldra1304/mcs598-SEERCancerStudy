# mcs598-SEERCancerStudy
Replication of the Paper: Reproducible Survival Prediction with SEER Cancer Data

This repository contains code and results from replicating the experimental setup outlined in in _Reproducible Survival Prediction with SEER Cancer Data_ submitted to the Machine Learning for Healthcare 2018 conference. (https://proceedings.mlr.press/v85/hegselmann18a/hegselmann18a.pdf, https://proceedings.mlr.press/v85/hegselmann18a/hegselmann18a-supp.pdf)

<ins>Repository Overview:</ins>
- **/_results**: Files used to perform manual steps and analysis of experimental results. attribute_table.xlsx and feature_mapping_table.pdf were used in creating the feature map between the 2016 database and the 2023 database. hyperparameters.xlsx was used for analysis of the tuning models. results_final.xlsx was used for analysis of the final models.
- **/_results/FINAL_MODELS**: Raw experimental results for 24 final models and combined_results.csv file which contains all validation and testing results.
- **/_results/TUNING**: Raw experimental results for 2,570 tuning models. Each of the 12 top-level folders contains a combined_results.csv file with the validation results for that model and cancer type. Survival durations are combined.
- **/cohort_2025**: SEER*Stat session files to reproduce data selections and original data exports from SEER*Stat for each session file.
- **/data_breast**: Converted input data for breast cancer analysis.
- **/data_lung**: Converted input data for lung and bronchus cancer analysis.
- **/lib**: Python classes and functions used for the experiments.
- **main.py**: Main routine to perform the experiments.
- **requirements.txt**: Python dependencies (can be installed with pip, e.g. in a virtual environment).

<ins>Additional Scripts:</ins>
- **attribute_importance_graphs.py**: Script to analyze the relative importance of attributes in the final models. 
- **collect_cluster_results_csv.py**: Script to parse all validation and test results in a folder structure and write to a csv file.
- **feature_analysis.py**: Script to perform socioeconomic feature vs. survivability analysis.
- **model_tuner.py**: Script to run model tuning. The model which is tuned depends on the provided commandline arguments.
- **run_final_models.py**: Script to run all final models.
- **sas_matrix_formatter.py**: Script to convert SEER*Stat case listing data exports into experiment's input data format.

<ins>Results Structure:</ins>
- **/[date_time]_exeriment-0/arguments.txt**: Commandline arguments for main.py call.
- **/[date_time]_exeriment-0/results_importance.txt**: Relative importance of each attribute in experiment. Only present if "--importance" argument supplied. 
- **/[date_time]_exeriment-0/results_test.txt**: AUC, F1, and ACC for test dataset. Used in final model testing. Only present if "--test" argument supplied.
- **/[date_time]_exeriment-0/results_validate.txt**: AUC, F1, and ACC for validation dataset. Used in model tuning. 


!!! OLD PAPER README.MD !!!
Repository overview:
- **/bin/cluster**: Slurm submission scripts for all parameter tuning experiments on the HPC cluster.
- **/cohort**: SEER*Stat session files to reproduce cohort selections.
- **/example**: Randomly generated SEER example to test the software without sensitive data.
- **/example/CASES.csv**: Example case export. To reproduce experiments, this should be generated for each cohort by loading the provided session files into SEER*Stat, executing the case listing, and exporting it via Matrix->Export->Results as Text File... with "CSV Defaults".
- **/example/INCIDENCES.txt**: Example SEER incidences. To reproduce experiments, this should contain all incidences provided by SEER 1973-2014 data (November 2016 submission) in ASCII format (e.g. by merging them into a single file). The according ASCII data files are available from SEER on request.
- **/lib**: Python classes and functions used for the experiments.
- **main.py**: Main routine to perform the experiments.
- **requirements.txt**: Python dependencies (can be installed with pip, e.g. in a virtual environment).


To execute main.py and reproduce our experiments Python3 (we used version 3.5.2) is necessary and all dependencies in requirements.txt must be satisfied. The easiest way would be to setup an according [virtual environment and to install requirements with pip](https://docs.python.org/3/tutorial/venv.html).

The option -h gives an overview of all command line arguments. Note that this code provides some additional functionality such as SVM models and survival regression that were not used for the paper's experiments.

```
$ python main.py -h
```

An experiment with the randomly generated examples and an MLP model can be performed as shown below. This will produce a folder in the current directory containing results and a plot for the AUC score.

```
$ python main.py --incidences example/INCIDENCES.txt --specifications example/read.seer.research.nov2016.sas --cases example/CASES.csv --task survival60 --oneHotEncoding --model MLP --mlpLayers 2 --mlpWidth 20 --mlpEpochs 1 --mlpDropout 0.1 --importance --plotData --plotResults
[...]
Read ASCII data files.
Raw data: (10000; 133) cases and attributes
Filtered SEER*Stat cases from ASCII: (5000; 133) cases and attributes
Remove irrelevant, combined, post-diagnosis, and treatment attributes: (5000; 960) cases and attributes
Create target label indicating cancer survival for survival60: (2831; 959) cases and attributes
Remove inputs with constant values: (2831; 925) cases and attributes
Data:  (2831, 925) -> x:(2831, 924), y:(2831,)
Train: x:(2264, 924), y:(2264,)
Valid: x:(283, 924), y:(283,)
Test:  x:(284, 924), y:(284,)

Train on 2264 samples, validate on 283 samples
Epoch 1/1
 - 1s - loss: 0.4241 - acc: 0.8913 - val_loss: 0.2623 - val_acc: 0.9293
Validation results: auc = 0.48878326996197724, f1 = 0.9633699633699635, acc = 0.9293286219081273
```
