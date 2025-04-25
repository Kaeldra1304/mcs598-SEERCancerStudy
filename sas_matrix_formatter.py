import sys

def sas_formatter(matrix_sas_file_path, insert_yr_birth_dx = True, debug = False) :

    # Read the matrix specifications file and extract data
    with open(matrix_sas_file_path, 'r') as matrix_sas_file:
    
        filename_in_file = ""
        in_format_section = False
        in_label_section = False
        matrix_var_dict = dict() # key: variable_name, value: string of last value found (NOT char length)
        matrix_lbl_dict = dict() # key: variable_name, value: string description of variable
        curr_var_name = ""
        for line in matrix_sas_file :
            # check for filename
            if "filename" in line :
                filename_in_file = line
        
            # check for section change
            if "proc format" in line :
                in_format_section = True
                in_label_section = False
                continue # continue to next line since format on own line
            elif "label" in line :
                in_format_section = False
                in_label_section = True
                line = line.replace("label","") # first label on same line as section header
            elif "run" in line :
                in_format_section = False
                in_label_section = False
                continue # continue to next line since run on own line
        
            # process line depending on section        
            if in_format_section == True :
                # 3 line formats:
                #  "value" contained in line with variable name
                #  "=" contained in line with variable values
                #  ";" to end that variable section            
                if debug : print("curr_var_name:", curr_var_name, "line:", line.strip())
                if ("value" in line) and ("=" not in line) : # "value" can be present in variable label strings
                    split_line = line.split()
                    if len(split_line) > 1 :
                        curr_var_name = (split_line[1].strip())[:-1] # removes last random character
                        matrix_var_dict[curr_var_name] = 0
                    else :
                        print("ERROR: Could not split \"value\" line...", line)
                        print(split_line)
                if "=" in line :
                    split_line = line.split("=")
                    val_str = split_line[0].strip()
                    if "-" in val_str :
                        val_str = ((val_str.split("-"))[1]).strip() # only save larger value in range
                    if curr_var_name != "" :
                        matrix_var_dict[curr_var_name] = val_str
                    else :
                        print("ERROR: Could not evaluate value from line...", line)
                        print(val_str, curr_var_name)
                        print(split_line)
                if ";" == line.strip() :
                    # end of variable section, clear current variable name
                    curr_var_name = ""
                    if debug : print("[reset curr_var_name]")

            elif in_label_section == True :            
                #  "=" contained in line with variable string descriptions
                if "=" in line :
                    split_line = line.split("=")
                    if len(split_line) == 2 :
                        matrix_lbl_dict[split_line[0].strip()] = (split_line[1].strip()).replace("\"", "")
                    else :
                        print("ERROR: Could not split label line...", line)
  

    # check for missing variable values
    for var_name_str_inVars in matrix_var_dict.keys() :
        if var_name_str_inVars not in matrix_lbl_dict :
            print("ERROR: Missing variable label:")
            print(var_name_str_inVars, "not in matrix_lbl_dict")

    # debugging print to console
    if debug : 
        for var_name_str, var_last_val_str in matrix_var_dict.items() :
            label_str = "ERROR"
            if var_name_str in matrix_lbl_dict :
                label_str = matrix_lbl_dict[var_name_str]
            print(var_name_str, var_last_val_str, label_str)


    # calculate position and variable length
    yr_birth_dx_inserted = False
    position = 1
    output_data_line = list() # list of tuple: (line_pos_str, var_name, char_len_str, var_label)
    for var_name_str, var_last_val_str in matrix_var_dict.items() :
        label_str = "ERROR"
        if var_name_str in matrix_lbl_dict :
            label_str = matrix_lbl_dict[var_name_str]
    
        char_len = len(var_last_val_str)
        output_data_line.append((str(position), var_name_str, str(char_len), label_str))
        position += char_len
                  
        # check for inserting year of birth at diagnosis calculated variable
        if (insert_yr_birth_dx == True) and (yr_birth_dx_inserted == False) :
            if "Age recode" in label_str :
                char_len = 4
                output_data_line.append((str(position), "YR_BRTH", str(char_len), "Year of birth"))
                position += char_len
                yr_birth_dx_inserted = True

    # now for writing format
    with open("matrix_reformat.sas", 'w') as matrix_format_file:
        matrix_format_file.write(filename_in_file) # has newline already appended
        matrix_format_file.write("\n")
        matrix_format_file.write("data in;" + "\n")
        matrix_format_file.write("  infile seer9 lrecl=" + str(position-1) + ";" + "\n")
        matrix_format_file.write("  input" + "\n")
        
        for (pos_str, name, len_str, lbl) in output_data_line :        
            matrix_format_file.write("    @ ")
            matrix_format_file.write(pos_str.ljust(len(str(position))+1)) # position padding width is 1 greater than max width
            matrix_format_file.write(name.ljust(50)) # hardcoded, names increased size (original: 21)
            matrix_format_file.write(("$char" + len_str + ".").ljust(9))
            matrix_format_file.write("/* " + lbl + " */")
            matrix_format_file.write("\n")

        matrix_format_file.write(";")
        
    # return output_data_line for parsing if needed
    return output_data_line

###### MAIN #######

debug_flag = False

# system args
matrix_file_path = "export.txt"
spec_file_path = "export.sas"
if len(sys.argv) >= 5: # program, "--matrix", matrix_file_path, "--specs", spec_file_path, "--debug"
    print(sys.argv)
    matrix_file_path = sys.argv[2]
    spec_file_path = sys.argv[4]
    if "--debug" in sys.argv :
        debug_flag = True
        
progress_interval = 10000
if debug_flag == True :
    progress_interval = 1000

# reformat SAS spec file for program use
# returns list of tuples: (line_pos_str, var_name, char_len_str, var_label)
output = sas_formatter(spec_file_path, debug = debug_flag)
print("sas formatter variable count:", len(output))

# parse formatter's output data for important variable indexes and char_spacing
char_spacing = []
yr_brth_idx = -1
age_dx_idx = -1
year_dx_idx = -1
patient_id_idx = -1
record_num_idx = -1

curr_idx = 0
for (line_pos_str, var_name, char_len_str, var_label) in output :
    char_spacing.append(int(char_len_str)) # record character spacing
    # search for data indexes
    if "Patient ID" in var_label :
        patient_id_idx = curr_idx
    elif ("Age" in var_label) and (age_dx_idx == -1) : # only find first age
        age_dx_idx = curr_idx
    elif "Year of birth" in var_label :
        yr_brth_idx = curr_idx
    elif "Year of diagnosis" in var_label : 
        year_dx_idx = curr_idx
    elif "Record number" in var_label :
        record_num_idx = curr_idx
    
    # next index
    curr_idx += 1
        
if debug_flag == True :
    print(char_spacing)
    print(yr_brth_idx,age_dx_idx,year_dx_idx,patient_id_idx,record_num_idx)
    #char_spacing_old = [8,1,2,1,3,4,2,3,3,1,4,1,1,1,1,4,3,3,2,2,2,1,2,2,2,4,4,4,3,4,4,4,4,4,4,4,3,3,3,3,2,2,2,2,2,2,2,3,1,3,2,2,2,2,2,3,3,1,2,2,3,1,1,1,2,3,3,2,1,3,3,1,1,2,3,2,1,1,2,2,2,1,1,1,2,4,4,4,4,4,4,2,4,1,4,4,4,4,3,3,3,3,3,4,4,1,1,2,2,2,2,2,3,3,3,2,2,2,2]


# read data from matrix.txt
# write INCIDENCES.csv file
line_num = 0
matrix_10_lines = list()
patient_ids_dict = dict()
with open(matrix_file_path, 'r') as matrix_file :
    with open('INCIDENCES.txt', 'w') as indicent_file :
        for line in matrix_file.readlines() :

            # skip header line
            if (line_num == 0) :
                line_num += 1
                continue
                
            # verification
            if line_num <= 10 :
                matrix_10_lines.append(line)
            
            # split csv into variables
            split_line = line.strip().split(",")
            #split_line = split_line[:-4] # ignore SEER*Stat added 4 extra columns, 
            #no longer needed HIDE column in SEER*Stat matrix before exporting
            
            # calculate year of birth = year of diagnosis - age of diagnosis
            age_dx = int(split_line[age_dx_idx])
            # year of diagnosis is stored as 3 char string (millenia + decade + year), need to add "0" for century
            #   (-1 in indexing is required since split_line does not contain yr_brth data yet)
            year_dx = int(split_line[year_dx_idx-1][0] + "0" + split_line[year_dx_idx-1][1:3])
            yr_brth = year_dx - age_dx # not perfect since month of diagnosis and month of birth are unknown            
            
            # insert calculated variable into split_line            
            split_line.insert(yr_brth_idx, str(yr_brth))
            
            # check for proper format
            if len(split_line) != (len(char_spacing)) :
                print("ERROR! Line Format Error")
                print("line:", line_num, len(char_spacing), len(split_line))

            # pad each variable with 0's
            patient_id = ""
            incidences_line = ""            
            for i in range(len(char_spacing)) :
                variable = split_line[i]
                while len(variable) < char_spacing[i] :
                    variable = "0" + variable
                incidences_line += variable
                
                # remember padded patient id for case file information
                if i == patient_id_idx : 
                    patient_id = variable
                    
                # save case file information to dictionary
                if i == record_num_idx :
                    patient_ids_dict[patient_id] = variable
        
            # write to incidences files
            indicent_file.write(incidences_line + "\n")
            
            # line number for progress bar
            if (line_num % progress_interval) == 0 :
                print("writing incidences line:", line_num)
            line_num += 1


# write CASES.csv file
print("writing cases file, total:", len(patient_ids_dict))
with open('CASES.csv', 'w') as cases_file :
    cases_file.write("Patient ID,Record number recode\n")
    for id_str, rec_num_str in patient_ids_dict.items() :
        cases_file.write(id_str + "," + rec_num_str + "\n")
        
if debug_flag == False :
    print()
    print("for debugging, turn on debug flag using \"--debug\"")

if debug_flag == True :        
    # formatting check by reading in incidences and writing out csv format for text compare of first 10 lines
    print("writing matrix_10.txt verification file", len(matrix_10_lines))
    with open('matrix_10.txt', 'w') as matrix10_file :
        for line in matrix_10_lines :
            matrix10_file.write(line)

    line_num = 0
    with open('INCIDENCES.txt', 'r') as incident_file :
        with open('verify.txt', 'w') as verify_file :
            with open('verify_10.txt', 'w') as verify10_file :
                for line in incident_file.readlines() :
            
                    verify_line = list()
                    position_index = 0
                    for i in range(len(char_spacing)) :
                        int_val = int(line[position_index:position_index+char_spacing[i]])
                        verify_line.append(str(int_val))
                        position_index += char_spacing[i]
                    verify_file.write(",".join(verify_line) + "\n")
                    if line_num < 10 :
                        verify10_file.write(",".join(verify_line) + "\n")
                
                    # line number for progress bar
                    if (line_num % progress_interval) == 0 :
                        print("writing verify line:", line_num)
                    line_num += 1