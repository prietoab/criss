import os
import yaml

# https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
#-------------------------------------------------------------------------
def getYAML(yamlFile):
#-------------------------------------------------------------------------
    with open(yamlFile, 'r') as stream:
        try:
            dictYAML = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            dictYAML = None
    return dictYAML 

#-------------------------------------------------------------------------
def get_file_names(path):
#-------------------------------------------------------------------------
    files_list = [name for name in os.listdir(path)]
    files_list.sort()
    return files_list, len(files_list)

#-------------------------------------------------------------------------
def isEven(num):
#-------------------------------------------------------------------------
    # Python program to check if the input number is odd or even.
    # A number is even if division by 2 gives a remainder of 0.
    # If the remainder is 1, it is an odd number.
    
#     if isinstance(num, int) == False:
#         print("Error. num is not a int")
#         return None
    
    if (num % 2) == 0:
       return True
    else:
       return False

#-------------------------------------------------------------------------
def getMaxEven(num):
#-------------------------------------------------------------------------
    int_num = int(num)
    if isEven(int_num):
        max_even = int_num
    else:
        max_even = int(int_num - 1)
    return max_even

#-------------------------------------------------------------------------
def getImageNamesListString(file_list):
#-------------------------------------------------------------------------
    str_list = []
    str_list.append("[")
    for file in file_list:
        str_list.append("'"+file+"'")
        str_list.append(",")
    str_list.pop()
    str_list.append("]") 
    return "".join(str_list)