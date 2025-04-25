import os
import matplotlib.pyplot as plt
import numpy as np
#output_dir = "C:\Users\Liz\Documents\Liz's\04Professional\masters_degree\CS598_DeepLearningHealthcare\proj\MLHC2018-reproducible-survival-seer-master\MLHC2018-reproducible-survival-seer-edits\FINAL_MODELS"

cancer_types = ["BREAST", "LUNG"]
survival_durations = [12, 60]
model_types = ["LogR", "LogREnc", "MLP", "MLPEnc", "MLPEmbEnc"]

for c_type in cancer_types :
    for task in survival_durations : 
        
        # read in data for each graph
        attribute_vals_dic = dict() # key: attribute string, value: numpy array of all values
        attribute_sum_dic = dict() # key: attribute string, value: float sum of all values
        for model_idx in range(len(model_types)) :
            model = model_types[model_idx]
            top_folder = c_type + "_" + str(task) + "_" + model
            dir_files = os.listdir("FINAL_MODELS/" + top_folder)
            if len(dir_files) > 0 : # check to make sure at 
                results_path = "FINAL_MODELS/" + top_folder + "/" + dir_files[0] + "/results_importance.txt"
                #print("~~~~~~~~~~~~~~")
                #print(top_folder)
                #print(results_path)
                
                # open file with results
                if os.path.exists(results_path):
                    with open(results_path, 'r') as results_file :
                        for line in results_file.readlines() :
                            if "=" in line :
                                split_line = line.split('=')
                                attribute_str = split_line[0]
                                attribute_val = float(split_line[1])
                                # store each value for later use
                                if attribute_str not in attribute_vals_dic :
                                    attribute_vals_dic[attribute_str] = np.zeros(len(model_types))
                                attribute_vals_dic[attribute_str][model_idx] = attribute_val
                                # store sum of values for attribute ranking
                                if attribute_str not in attribute_sum_dic :
                                    attribute_sum_dic[attribute_str] = 0.0
                                attribute_sum_dic[attribute_str] += attribute_val
                else :
                    print("ERROR: No Results File!", results_path)
            else :
                print("ERROR: No Experiment Run!", top_folder)

        # find top ten attributes based on their sum for all models
        top_10_attributes = list(dict(sorted(attribute_sum_dic.items(), key=lambda item: item[1], reverse=True)[:10]).keys())
        print()
        print("Top 10 SEER Attributes,", c_type, "Cancer", str(int(task/12))+"-yr Survival")
        for i in range(len(top_10_attributes)) :
            print(str(i+1) + ")", top_10_attributes[i])
        
        # create numpy arrays for graphing
        data_arrays_dict = dict() # key: model name, value: len 10 array of floats 
        for model_idx in range(len(model_types)) :
            model = model_types[model_idx]
            data_arrays_dict[model] = np.zeros(len(top_10_attributes)) # initialize data array
            for attribute_idx in range(len(top_10_attributes)) :
                attribute = top_10_attributes[attribute_idx]
                val = attribute_vals_dic[attribute][model_idx]
                data_arrays_dict[model][attribute_idx] = val # set value in data arrays
                
        # plot
        x = np.arange(len(top_10_attributes))  # the label locations
        width = 0.15  # the width of the bars, originally 0.25
        multiplier = -1 # originally 0
        
        fig, ax = plt.subplots(layout='tight')
        fig.set_figheight(5) # Set the height to 5 inches
        ax.grid(True, zorder=0)
        measurement_max = 0
        for attribute, measurement in data_arrays_dict.items():
            offset = width * multiplier
            #rects = ax.bar(x + offset, measurement, width, label=attribute) # vertical
            rects = ax.barh(x + offset, measurement, width, label=attribute) # horizontal
            if measurement.max() > measurement_max :
                measurement_max = measurement.max()
            #ax.bar_label(rects, padding=3)
            multiplier += 1
        
        # Vertical Bars
        # Add some text for labels, title and custom x-axis tick labels, etc.
        #ax.set_xlabel('Attribute Rank')
        #ax.set_ylabel('Relative Importance')
        #ax.set_xticks(x + width, (s.replace(" ", "\n") for s in top_10_attributes)) # use newline to display labels better
        #ax.yaxis.set_ticks(np.arange(0, measurement_max + 0.01, 0.01))
        
        # Horizontal Bars
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Attribute Rank')
        ax.set_xlabel('Relative Importance')
        ax.set_yticks(x + width, (str(i+1) for i in range(len(top_10_attributes)))) # use newline to display labels better
        ax.xaxis.set_ticks(np.arange(0, measurement_max + 0.01, 0.01))
        
        #ax.set_title('Top 10 Attributes')
        #ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncols=len(model_types))
        ax.legend(loc='best')
        plt.show()

