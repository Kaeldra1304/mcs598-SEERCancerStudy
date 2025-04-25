import subprocess
import sys
import os
    
breast_specs = "data_breast/matrix_reformat.sas"
breast_data = "data_breast/INCIDENCES.txt"
breast_cases = "data_breast/CASES.csv"
lung_specs = "data_lung/matrix_reformat.sas"
lung_data = "data_lung/INCIDENCES.txt"
lung_cases = "data_lung/CASES.csv"

# create common parameter arrays
#header_array = ["python", "main.py", "--output", "FINAL_MODELS"]
header_array = ["python", "main.py"]
files_breast_array = ["--incidences", breast_data, "--specifications", breast_specs, "--cases", breast_cases]
files_lung_array = ["--incidences", lung_data, "--specifications", lung_specs, "--cases", lung_cases]

# initialize list of all processes to run
subprocesses_list = list()

# DBUGGING
#reg_param_C = -1
#mlp_num_layers = -1
#mlp_width_val = -1
#mlp_num_epochs = -1
#mlp_dropout_val = -1
#mlpemb_num_neurons = -1

# 24 iterations to run, 12 breast & 12 lung

# BREAST CANCER

# 1B) BASE, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_NAIVE"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "NAIVE"])
subprocesses_list.append(process_array)

# 2B) BASE, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_NAIVE"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "NAIVE"])
subprocesses_list.append(process_array)

# 3B) LOG REG, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_LogR"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(0.1)])
subprocesses_list.append(process_array)

# 4B) LOG REG, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_LogR"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(0.01)])
subprocesses_list.append(process_array)

# 5B) LOG REG + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_LogREnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(0.1)])
subprocesses_list.append(process_array)

# 6B) LOG REG + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_LogREnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(0.1)])
subprocesses_list.append(process_array)

# 7B) MLP, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_MLP"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(1)])
process_array.extend(["--mlpWidth", str(100)])
process_array.extend(["--mlpEpochs", str(20)])
process_array.extend(["--mlpDropout", str(0.2)])
subprocesses_list.append(process_array)

# 8B) MLP, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_MLP"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(1)])
process_array.extend(["--mlpWidth", str(100)])
process_array.extend(["--mlpEpochs", str(20)])
process_array.extend(["--mlpDropout", str(0.2)])
subprocesses_list.append(process_array)

# 9B) MLP + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_MLPEnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(1)]) 
process_array.extend(["--mlpWidth", str(20)])
process_array.extend(["--mlpEpochs", str(20)]) 
process_array.extend(["--mlpDropout", str(0.5)]) 
subprocesses_list.append(process_array)

# 10B) MLP + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_MLPEnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(1)]) 
process_array.extend(["--mlpWidth", str(20)]) 
process_array.extend(["--mlpEpochs", str(20)])
process_array.extend(["--mlpDropout", str(0.2)])
subprocesses_list.append(process_array)

# 11B) MLPEmb + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_12_MLPEmbEnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLPEmb"])
process_array.extend(["--mlpLayers", str(2)])
process_array.extend(["--mlpWidth", str(50)])
process_array.extend(["--mlpEpochs", str(20)])
process_array.extend(["--mlpDropout", str(0.3)])
process_array.extend(["--mlpEmbNeurons", str(3)])
subprocesses_list.append(process_array)

# 12B) MLPEmb + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/BREAST_60_MLPEmbEnc"])
process_array.extend(files_breast_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLPEmb"])
process_array.extend(["--mlpLayers", str(1)])
process_array.extend(["--mlpWidth", str(20)])
process_array.extend(["--mlpEpochs", str(20)])
process_array.extend(["--mlpDropout", str(0.4)])
process_array.extend(["--mlpEmbNeurons", str(10)])
subprocesses_list.append(process_array)



# LUNG CANCER

# 1L) BASE, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_NAIVE"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "NAIVE"])
subprocesses_list.append(process_array)

# 2L) BASE, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_NAIVE"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "NAIVE"])
subprocesses_list.append(process_array)

# 3L) LOG REG, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_LogR"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(10000)])
subprocesses_list.append(process_array)

# 4L) LOG REG, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_LogR"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(10000000000)])
subprocesses_list.append(process_array)

# 5L) LOG REG + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_LogREnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(0.1)])
subprocesses_list.append(process_array)

# 6L) LOG REG + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_LogREnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "LogR"])
process_array.extend(["--logrC", str(1)])
subprocesses_list.append(process_array)

# 7L) MLP, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_MLP"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(3)])
process_array.extend(["--mlpWidth", str(100)])
process_array.extend(["--mlpEpochs", str(100)])
process_array.extend(["--mlpDropout", str(0.2)])
subprocesses_list.append(process_array)

# 8L) MLP, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_MLP"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(3)]) 
process_array.extend(["--mlpWidth", str(100)]) 
process_array.extend(["--mlpEpochs", str(100)])
process_array.extend(["--mlpDropout", str(0.5)]) 
subprocesses_list.append(process_array)

# 9L) MLP + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_MLPEnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(3)])
process_array.extend(["--mlpWidth", str(20)])
process_array.extend(["--mlpEpochs", str(100)])
process_array.extend(["--mlpDropout", str(0.3)])
subprocesses_list.append(process_array)

# 10L) MLP + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_MLPEnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLP"])
process_array.extend(["--mlpLayers", str(4)])
process_array.extend(["--mlpWidth", str(20)])
process_array.extend(["--mlpEpochs", str(100)])
process_array.extend(["--mlpDropout", str(0.5)])
subprocesses_list.append(process_array)

# 11L) MLPEmb + 1-N ENC, 1-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_12_MLPEmbEnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival12"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLPEmb"])
process_array.extend(["--mlpLayers", str(3)])
process_array.extend(["--mlpWidth", str(20)]) 
process_array.extend(["--mlpEpochs", str(100)]) 
process_array.extend(["--mlpDropout", str(0.2)]) 
process_array.extend(["--mlpEmbNeurons", str(10)]) 
subprocesses_list.append(process_array)

# 12L) MLPEmb + 1-N ENC, 5-YR SURVIVAL
process_array = list()
process_array.extend(header_array)
process_array.extend(["--output", "FINAL_MODELS/LUNG_60_MLPEmbEnc"])
process_array.extend(files_lung_array)
process_array.extend(["--task", "survival60"])
process_array.append("--oneHotEncoding")
process_array.append("--test")
process_array.append("--importance")
process_array.extend(["--model", "MLPEmb"])
process_array.extend(["--mlpLayers", str(4)]) 
process_array.extend(["--mlpWidth", str(20)]) 
process_array.extend(["--mlpEpochs", str(50)])
process_array.extend(["--mlpDropout", str(0.4)])
process_array.extend(["--mlpEmbNeurons", str(3)])
subprocesses_list.append(process_array)


for i in range(len(subprocesses_list)) :
    process_array = subprocesses_list[i]
    # run (or print) subprocess                                    
    subprocess.run(process_array)
    print("***** subprocess", i+1, "complete *****")
    #print(",".join(process_array))
    #os.makedirs(process_array[3], exist_ok=True)

print("TOTAL:", len(subprocesses_list))


# output 4/14/2025 11:17AM
"""
python,main.py,--output,FINAL_MODELS/BREAST_12_NAIVE,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--test,--importance,--model,NAIVE
python,main.py,--output,FINAL_MODELS/BREAST_60_NAIVE,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--test,--importance,--model,NAIVE
python,main.py,--output,FINAL_MODELS/BREAST_12_LogR,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--test,--importance,--model,LogR,--logrC,0.1
python,main.py,--output,FINAL_MODELS/BREAST_60_LogR,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--test,--importance,--model,LogR,--logrC,0.01
python,main.py,--output,FINAL_MODELS/BREAST_12_LogREnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,LogR,--logrC,0.1
python,main.py,--output,FINAL_MODELS/BREAST_60_LogREnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,LogR,--logrC,0.1
python,main.py,--output,FINAL_MODELS/BREAST_12_MLP,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--test,--importance,--model,MLP,--mlpLayers,1,--mlpWidth,100,--mlpEpochs,20,--mlpDropout,0.2
python,main.py,--output,FINAL_MODELS/BREAST_60_MLP,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--test,--importance,--model,MLP,--mlpLayers,1,--mlpWidth,100,--mlpEpochs,20,--mlpDropout,0.2
python,main.py,--output,FINAL_MODELS/BREAST_12_MLPEnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,MLP,--mlpLayers,1,--mlpWidth,20,--mlpEpochs,20,--mlpDropout,0.5
python,main.py,--output,FINAL_MODELS/BREAST_60_MLPEnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,MLP,--mlpLayers,1,--mlpWidth,20,--mlpEpochs,20,--mlpDropout,0.2
python,main.py,--output,FINAL_MODELS/BREAST_12_MLPEmbEnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,MLPEmb,--mlpLayers,2,--mlpWidth,50,--mlpEpochs,20,--mlpDropout,0.3,--mlpEmbNeurons,3
python,main.py,--output,FINAL_MODELS/BREAST_60_MLPEmbEnc,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,MLPEmb,--mlpLayers,1,--mlpWidth,20,--mlpEpochs,20,--mlpDropout,0.4,--mlpEmbNeurons,10
python,main.py,--output,FINAL_MODELS/LUNG_12_NAIVE,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--test,--importance,--model,NAIVE
python,main.py,--output,FINAL_MODELS/LUNG_60_NAIVE,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--test,--importance,--model,NAIVE
python,main.py,--output,FINAL_MODELS/LUNG_12_LogR,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--test,--importance,--model,LogR,--logrC,10000
python,main.py,--output,FINAL_MODELS/LUNG_60_LogR,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--test,--importance,--model,LogR,--logrC,10000000000
python,main.py,--output,FINAL_MODELS/LUNG_12_LogREnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,LogR,--logrC,0.1
python,main.py,--output,FINAL_MODELS/LUNG_60_LogREnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,LogR,--logrC,1
python,main.py,--output,FINAL_MODELS/LUNG_12_MLP,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--test,--importance,--model,MLP,--mlpLayers,3,--mlpWidth,100,--mlpEpochs,100,--mlpDropout,0.2
python,main.py,--output,FINAL_MODELS/LUNG_60_MLP,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--test,--importance,--model,MLP,--mlpLayers,3,--mlpWidth,100,--mlpEpochs,100,--mlpDropout,0.5
python,main.py,--output,FINAL_MODELS/LUNG_12_MLPEnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,MLP,--mlpLayers,3,--mlpWidth,20,--mlpEpochs,100,--mlpDropout,0.3
python,main.py,--output,FINAL_MODELS/LUNG_60_MLPEnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,MLP,--mlpLayers,4,--mlpWidth,20,--mlpEpochs,100,--mlpDropout,0.5
python,main.py,--output,FINAL_MODELS/LUNG_12_MLPEmbEnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--test,--importance,--model,MLPEmb,--mlpLayers,3,--mlpWidth,20,--mlpEpochs,100,--mlpDropout,0.2,--mlpEmbNeurons,10
python,main.py,--output,FINAL_MODELS/LUNG_60_MLPEmbEnc,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--test,--importance,--model,MLPEmb,--mlpLayers,4,--mlpWidth,20,--mlpEpochs,50,--mlpDropout,0.4,--mlpEmbNeurons,3
TOTAL: 24
"""

# output 4/11/2025 11:03AM
"""
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--model,NAIVE
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--model,NAIVE
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival12,--oneHotEncoding,--model,MLPEmb,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1,--mlpEmbNeurons,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_breast.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_breast.csv,--task,survival60,--oneHotEncoding,--model,MLPEmb,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1,--mlpEmbNeurons,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--model,NAIVE
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--model,NAIVE
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--model,LogR,--logrC,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--model,MLP,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival12,--oneHotEncoding,--model,MLPEmb,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1,--mlpEmbNeurons,-1
python,main.py,--output,FINAL_MODELS,--incidences,data/INCIDENCES_lung.txt,--specifications,data/matrix_reformat.sas,--cases,data/CASES_lung.csv,--task,survival60,--oneHotEncoding,--model,MLPEmb,--mlpLayers,-1,--mlpWidth,-1,--mlpEpochs,-1,--mlpDropout,-1,--mlpEmbNeurons,-1
"""

# run .csv creator in FINAL_MODELS dir

# .csv creator should output runtime and results

# graph attribute importance
