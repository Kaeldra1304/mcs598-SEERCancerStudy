import subprocess
import sys

batch_type_to_run = 0 # default to example
if len(sys.argv) >= 7: # program, "--type", type_val, "--task", task_val, "--data", data_type_str
    print(sys.argv)
    batch_type_to_run = int(sys.argv[2])
    task_length_to_run = int(sys.argv[4])
    data_type = sys.argv[6]
    
incidences_path = "data_" + data_type + "/INCIDENCES.txt" # possibly sys args
specs_path = "data_" + data_type + "/matrix_reformat.sas" # possibly sys args
cases_path = "data_" + data_type + "/CASES.csv" # possibly sys args

# initialize list of all processes to run
subprocesses_list = list()

# initialize all adjustable parameters
output_dir = "default"
task = "survival" + str(task_length_to_run)
oneHotEnc_flag = False
model = "NAIVE"
logrc_list = [1.0]
mlp_layers_list = [1]
mlp_width_list = [1]
mlp_dropout_list = [0.0]
mlp_epochs_list = [1]
mlpemb_neurons_list = [1]

# different types of batches to run
# nothing to tune for NAIVE model
TYPE_EXAMPLE = 0 # not used in this script
TYPE_FINAL_MODELS = 1 # not used in this script
TYPE_TUNE_LOGREG = 2
TYPE_TUNE_LOGREG_1ENC = 3
TYPE_TUNE_MLP = 4
TYPE_TUNE_MLP_1ENC = 5
TYPE_TUNE_MLPEMB_1ENC = 6

# change parameters based on batch type
# FINAL MODELS

# LOGISTIC REGRESSION 
if batch_type_to_run == TYPE_TUNE_LOGREG :
    output_dir = "TUNING/Tuning_LogR_" + data_type
    oneHotEnc_flag = False
    model = "LogR"
    logrc_list = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0, 100000000.0, 1000000000.0, 10000000000.0]
    mlp_layers_list = [1]
    mlp_width_list = [1]
    mlp_dropout_list = [0.0]
    mlp_epochs_list = [1]
    mlpemb_neurons_list = [1]
    
# LOGISTIC REGRESSION W/ 1-N ENCODING
if batch_type_to_run == TYPE_TUNE_LOGREG_1ENC :
    output_dir = "TUNING/Tuning_LogR_Enc_" + data_type
    oneHotEnc_flag = True
    model = "LogR"
    logrc_list = [0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0, 100000000.0, 1000000000.0, 10000000000.0]
    mlp_layers_list = [1]
    mlp_width_list = [1]
    mlp_dropout_list = [0.0]
    mlp_epochs_list = [1]
    mlpemb_neurons_list = [1]

# MLP
if batch_type_to_run == TYPE_TUNE_MLP :
    output_dir = "TUNING/Tuning_MLP_" + data_type
    oneHotEnc_flag = False
    model = "MLP"
    logrc_list = [1.0]
    mlp_layers_list = [1, 2, 3, 4]
    mlp_width_list = [20, 50, 100, 200]
    mlp_dropout_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    mlp_epochs_list = [20, 50, 100] # start with just tuning on 20 epochs due to limited resources
    mlpemb_neurons_list = [1]

# MLP W/ 1-N ENCODING
if batch_type_to_run == TYPE_TUNE_MLP_1ENC :
    output_dir = "TUNING/Tuning_MLP_Enc_" + data_type
    oneHotEnc_flag = True
    model = "MLP"
    logrc_list = [1.0]
    mlp_layers_list = [1, 2, 3, 4]
    mlp_width_list = [20, 50, 100, 200]
    mlp_dropout_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    mlp_epochs_list = [20, 50, 100] # start with just tuning on 20 epochs due to limited resources
    mlpemb_neurons_list = [1]

# MLP EMBEDDING W/ 1-N ENCODING
if batch_type_to_run == TYPE_TUNE_MLPEMB_1ENC :
    output_dir = "TUNING/Tuning_MLPEmb_Enc_" + data_type
    oneHotEnc_flag = True
    model = "MLPEmb"
    logrc_list = [1.0]
    
    # defaults, running all combinations (864 per task/data_type => 3,456)
    mlp_layers_list = [1, 2, 3, 4]
    mlp_width_list = [20, 50, 100, 200]
    mlp_dropout_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    mlp_epochs_list = [20, 50, 100]
    mlpemb_neurons_list = [3, 5, 10]
    
    # four different sets of parameters due to large combo sets
    # based on results of TYPE_TUNE_MLP_1ENC per task/data_type
    if (data_type == "breast") and (task == "survival12") :
        mlp_layers_list = [1, 2]
        mlp_width_list = [20, 50]
        mlp_dropout_list = [0.3, 0.4, 0.5]
        mlp_epochs_list = [20]
        mlpemb_neurons_list = [3, 5, 10]
    elif (data_type == "breast") and (task == "survival60") :
        mlp_layers_list = [1]
        mlp_width_list = [20, 50]
        mlp_dropout_list = [0.2, 0.3, 0.4]
        mlp_epochs_list = [20, 50, 100]
        mlpemb_neurons_list = [3, 5, 10]
    elif (data_type == "lung") and (task == "survival12") :
        mlp_layers_list = [2, 3]
        mlp_width_list = [20, 50]
        mlp_dropout_list = [0.2, 0.3, 0.5]
        mlp_epochs_list = [100]
        mlpemb_neurons_list = [3, 5, 10]
    elif (data_type == "lung") and (task == "survival60") :
        mlp_layers_list = [3, 4]
        mlp_width_list = [20]
        mlp_dropout_list = [0.2, 0.4, 0.5]
        mlp_epochs_list = [20, 50]
        mlpemb_neurons_list = [3, 5, 10]


# massive nested-for loop over all changeable parameters
for reg_param_C in logrc_list :
    for mlp_num_layers in mlp_layers_list :
        for mlp_width_val in mlp_width_list :
            for mlp_dropout_val in mlp_dropout_list :
                for mlp_num_epochs in mlp_epochs_list :
                    for mlpemb_num_neurons in mlpemb_neurons_list :
                        process_array = list()
                        process_array.append("python")
                        process_array.append("main.py")
                        process_array.append("--output")
                        process_array.append(output_dir)
                        process_array.append("--incidences")
                        process_array.append(incidences_path)
                        process_array.append("--specifications")
                        process_array.append(specs_path)
                        process_array.append("--cases")
                        process_array.append(cases_path)
                        process_array.append("--task")
                        process_array.append(task)
                        if oneHotEnc_flag == True :
                            process_array.append("--oneHotEncoding")
                        process_array.append("--model")
                        process_array.append(model)
                        process_array.append("--logrC")
                        process_array.append(str(reg_param_C))
                        process_array.append("--mlpLayers")
                        process_array.append(str(mlp_num_layers))
                        process_array.append("--mlpWidth")
                        process_array.append(str(mlp_width_val))
                        process_array.append("--mlpEpochs")
                        process_array.append(str(mlp_num_epochs))
                        process_array.append("--mlpDropout")
                        process_array.append(str(mlp_dropout_val))
                        process_array.append("--mlpEmbNeurons")
                        process_array.append(str(mlpemb_num_neurons))
                                    
                        # add process_array to subprocesses_list
                        subprocesses_list.append(process_array)

for i in range(len(subprocesses_list)) :
    process_array = subprocesses_list[i]
    # run (or print) subprocess                                    
    subprocess.run(process_array)
    #print(",".join(process_array))
    print("***** subprocess", i+1, "complete *****")

print("TOTAL:", len(subprocesses_list))

"""# example
process_array = list()
process_array.append("python")
process_array.append("main.py")
process_array.append("--output")
process_array.append("Tuning")
process_array.append("--incidences")
process_array.append("data/INCIDENCES.txt")
process_array.append("--specifications")
process_array.append("data/matrix_reformat.sas")
process_array.append("--cases")
process_array.append("data/CASES.csv")
process_array.append("--task")
process_array.append("survival60")
process_array.append("--oneHotEncoding")
process_array.append("--model")
process_array.append("MLP")
process_array.append("--mlpLayers")
process_array.append("2")
process_array.append("--mlpWidth")
process_array.append("20")
process_array.append("--mlpEpochs")
process_array.append("1")
process_array.append("--mlpDropout")
process_array.append("0.1")
process_array.append("--importance")

subprocess.run(process_array)"""

# process results
# currently prints csv to console
# could make collect_cluster_results.py write to .csv file
# could also run command as subprocess
#"python collect_cluster_results_csv.py [folder]"