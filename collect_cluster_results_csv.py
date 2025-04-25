""" A short helper script that collects the results of the cluster jobs and format them correctly as CSV. """
import sys
import time
import os


def main():
    with open('combined_results.csv', 'w') as results_file :
        # Directory with the cluster output
        cluster_output = sys.argv[1] + ('' if sys.argv[1][-1] == '/' else '/')
        if "\\" in cluster_output :
            cluster_output = cluster_output.replace("\\", "/")
        print("Cluster Directory:", cluster_output)

        # Determine columns.
        argument_columns = ['task', 'model', 'oneHotEncoding',
                            'mlpLayers', 'mlpWidth', 'mlpDropout', 'mlpEpochs',
                            'mlpEmbNeurons', 'logrC']
        result_columns = ['auc', 'f1', 'acc', 'set']
        test_results_columns = ['test_' + c for c in result_columns]
        
        # write header
        header_str = 'folder,'
        header_str = header_str + ','.join(argument_columns) + ','
        header_str = header_str + ','.join(result_columns) + ','
        header_str = header_str + ','.join(test_results_columns) + ','
        header_str += 'auc+f1'
        results_file.write(header_str + '\n')

        scores = []
        
        # this allows for subdirectories & recursion
        # scans for "_experiment-" directories
        results_folder_tag = "_experiment-"
        results_folders_list = list()
        dir_index = 0
        dir_list = [ f.path for f in os.scandir(cluster_output) if f.is_dir() ] # seed list of top level folders

        while dir_index < len(dir_list) :
            dir_idx_path = dir_list[dir_index]            
            if results_folder_tag in dir_idx_path :
                results_folders_list.append(dir_idx_path)
            else :
                dir_list.extend([ f.path for f in os.scandir(dir_idx_path) if f.is_dir() ])
            dir_index += 1
    
        # loop through results folders
        for results_path in results_folders_list :
            if (".csv" in results_path) :
                print("excluding file", results_path, "...")
                continue
            
            # Now inside a single run output.

            # Read in arguments.
            arguments = {}
            #arguments_path = cluster_output + output_dir + '/arguments.txt'
            arguments_path = results_path + '/arguments.txt'
            if os.path.isfile(arguments_path):
                with open(arguments_path, 'r') as cluster_output_arguments:
                    for line in cluster_output_arguments:
                        line = line.rstrip()

                        if ":" not in line:
                            continue
                        if line.startswith("#"):
                            continue

                        k, v = line.split(":", 1)
                        arguments[k.strip()] = v.strip()

            # Read in results.
            valid_results = {}
            #validate_path = cluster_output + output_dir + '/results_validate.txt'
            validate_path = results_path + '/results_validate.txt'
            if os.path.isfile(validate_path):
                with open(validate_path, 'r') as cluster_output_results:
                    for line in cluster_output_results:
                        line = line.rstrip()

                        if "=" not in line:
                            continue
                        if line.startswith("#"):
                            continue

                        k, v = line.split("=", 1)
                        valid_results[k.strip()] = v.strip()

            # Read in test results.
            test_results = {}
            #test_path = cluster_output + output_dir + '/results_test.txt'
            test_path = results_path + '/results_test.txt'
            if os.path.isfile(test_path):
                with open(test_path, 'r') as cluster_output_results:
                    for line in cluster_output_results:
                        line = line.rstrip()

                        if "=" not in line:
                            continue
                        if line.startswith("#"):
                            continue

                        k, v = line.split("=", 1)
                        test_results[k.strip()] = v.strip()

            # Build value column
            line = ''
            #line += output_dir + ','
            results_sub_dir = results_path[results_path[:results_path.rfind("\\")].rfind("/")+1:] # find 2nd to last dir
            line += results_sub_dir + ','

            for arg in argument_columns:
                line += (arguments[arg] if arg in arguments else '') + ','

            for res in result_columns:
                line += (valid_results[res] if res in valid_results else '') + ','

            for res in result_columns:
                line += (test_results[res] if res in test_results else '') + ','

            auc = float(valid_results['auc'] if 'auc' in valid_results else '-10')
            f1 = float(valid_results['f1'] if 'f1' in valid_results else '-10')
            scores.append((line, auc + f1))

        scores.sort(key=lambda x: x[1], reverse=True)

        for (line, score) in scores:
            results_file.write(line + str(score) + '\n')


if __name__ == "__main__":
    main()
