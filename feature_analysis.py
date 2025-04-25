import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

def GrabDataFromLine(line, data_tuple, debug = False) :
        
    start = int(data_tuple[0]) - 1 # data tuple contains position, subtract 1 to convert to string index
    end = start + int(data_tuple[1])    
    
    if debug == True:
        print(data_tuple)
        print(start, end)
        print(line[start:end])
    
    return int(line[start:end])

debug_flag = False
specs_path = "data/matrix_reformat.sas"
data_path = "data/INCIDENCES.txt"

if len(sys.argv) >= 5: # program, "--spec", specs_path, "--data", data_path
    print(sys.argv)
    specs_path = sys.argv[2]
    data_path = sys.argv[4]

# read in specifications file
specs_dict = dict()
with open(specs_path, 'r') as specs_file :
    position_str = '@'
    length_str = '$char'
    label_str = '/*'
    
    for line in specs_file.readlines() :
        #print("line:",line)
        if (position_str in line) and (length_str in line) and (label_str in line) :
            data_pos = -1
            data_len = -1
            data_label = ""
            
            # split off label first since it may contain whitespace
            label_split_line = line.split(label_str)
            if len(label_split_line) != 2 :
                print("ERROR: extra/missing label marker", label_str, "in line/n", line)
            else :
                data_label = label_split_line[1].replace('*/','').replace(';','').strip()
                #print(data_label)
            
                # split the rest of line by spaces
                data_split_line = label_split_line[0].split()
                if data_split_line[0] != position_str :
                    print("ERROR: missing", position_str, "in line/n", line)
                elif length_str not in data_split_line[3] :
                    print("ERROR: missing", length_str, "in line/n", line)
                else :
                    # correct formatting
                    #print(data_split_line[1], data_split_line[3])
                    data_pos = int(data_split_line[1].strip())
                    data_len = int(data_split_line[3].replace(length_str,'').replace('.','').strip())
                    specs_dict[data_label] = (data_pos, data_len)
        #else :
            #print("can't find formatting strings", position_str, length_str, label_str)
                    
# debugging print to console
if debug_flag == True :
    for label_str in specs_dict.keys() :
        print(label_str + ":", specs_dict[label_str])
    print("TOTAL VARIABLES:", len(specs_dict))    


# Features to Analyze
#    @ 297 XMHIIA               $char2.  /* Median household income inflation adj to 2022 */ 
#    @ 299 XRUCC                $char2.  /* Rural-Urban Continuum Code */
# Target Features
#    @ 228 SRV_TIME_MON         $char4.  /* Survival months */ 
#    @ 232 SRV_TIME_MON_FLAG    $char1.  /* Survival months flag */  (filter only! uses data if value 0 or 1)

features_lbl_list = ["Median household income inflation adj to 2022", "Rural-Urban Continuum Code"]
features_ranges_list = [[0,18], [0,10]]
target_feature_lbl = "Survival months"
target_flag_lbl = "Survival months flag"
target_flag_vals = [0, 1]

data_dict = dict() # dictionary of lists, one for each feature
data_dict["Survival months"] = list()
for i in range(len(features_lbl_list)) :
    data_dict[features_lbl_list[i]] = list()

# read in data file in original ASCII format
with open(data_path, 'r') as data_file :
    case_idx = 0
    for line in data_file.readlines() :
        line = line.strip()
        # find target flag first, make sure it is in usable range
        target_flag = GrabDataFromLine(line, specs_dict[target_flag_lbl])
        
        if (debug_flag == True) and (case_idx == 0) :
            print(line)
            print(GrabDataFromLine(line, specs_dict[target_flag_lbl], debug = debug_flag))
            print(GrabDataFromLine(line, specs_dict[target_feature_lbl], debug = debug_flag))
            print(GrabDataFromLine(line, specs_dict[features_lbl_list[0]], debug = debug_flag))
            print(GrabDataFromLine(line, specs_dict[features_lbl_list[1]], debug = debug_flag))
            
        if target_flag in target_flag_vals :
            
            # add entry to dynamic lists
            for key in data_dict.keys() :
                data_dict[key].append(0)
                
            # grab target data
            target = GrabDataFromLine(line, specs_dict[target_feature_lbl])
            data_dict[target_feature_lbl][case_idx] = target
            
            # grab feature data
            for i in range(len(features_lbl_list)) :
                feature_lbl = features_lbl_list[i]
                feature = GrabDataFromLine(line, specs_dict[feature_lbl])
                data_dict[feature_lbl][case_idx] = feature
            
            # incement case index
            case_idx += 1


# plot data scatter plots
for i in range(len(features_lbl_list)) :
    feature_lbl = features_lbl_list[i]    
    
    x = np.array(data_dict[feature_lbl])
    y = np.array(data_dict[target_feature_lbl])
    
    # plot data scatter plot
    plt.scatter(x, y, s = 4, alpha = 0.01)
    
    # Calculate the Pearson correlation coefficient (r)
    correlation, _ = pearsonr(x, y)
    print("CORRELATION (R):", correlation)

    # calc data statistics by group
    x_unique_vals = np.unique(x)
    x_means = np.zeros(len(x_unique_vals))
    x_stds = np.zeros(len(x_unique_vals))
        
    for v in range(len(x_unique_vals)):
        group = x_unique_vals[v]        
        group_data = y[np.where(x == group)]
        x_means[v] = np.mean(group_data)
        x_stds[v] = np.std(group_data)
        

    # overlay statistics as second scatter plot
    plt.scatter(x_unique_vals, x_means, c='yellow', marker='_', label='mean')
    plt.scatter(x_unique_vals, x_means + x_stds, c='red', marker='_', label='+1 std')
    plt.scatter(x_unique_vals, x_means - x_stds, c='orange', marker='_', label='-1 std')

    # Add a legend
    plt.legend(loc='lower right')     

    # Add labels and title
    plt.xlabel(feature_lbl)
    plt.ylabel(target_feature_lbl)
    plt.title(feature_lbl + " vs " + target_feature_lbl)
    
    # Adjust axis ranges
    plt.xlim(features_ranges_list[i][0], features_ranges_list[i][1])

    # Show the plot
    plt.show()
  
# debug plot  
# plot scatter plots
#plt.scatter(np.array(data_dict["Median household income inflation adj to 2022"]), np.array(data_dict["Rural-Urban Continuum Code"]), alpha = 0.01)
#plt.xlim(0, 20)
#plt.ylim(0, 10)
# Show the plot
#plt.show()