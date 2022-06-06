from difflib import SequenceMatcher 
import os


# path = 'data-thesis'
# sub_dir = os.listdir(path)
# list = [(x) for x in sub_dir if os.path.isdir(path+"/"+x) and x!='.git' and x!='1-data-scripts']
# print(list)

def check(fileName1, fileName2): 
    with open(fileName1, errors='ignore') as file_1,open(fileName2, errors='ignore') as file_2: 
        file1_data = file_1.read() 
        file2_data = file_2.read() 
        similarity_ratio = SequenceMatcher(None,file1_data,file2_data).ratio() 
    return similarity_ratio

root_dir = "folderpath"
file_list = []

for dir_, _, files in os.walk(root_dir):
    for file_name in files:
        rel_dir = os.path.relpath(dir_, root_dir)
        file_list.append(root_dir + file_name)


    
list_length = len(file_list)
duplicates = []
temp = 0

print("looking for duplicates in "+ root_dir)

for i in file_list:
    for j in file_list:
        if i!=j:
            if check(i, j) >= .98:
                duplicates.append(j)
                file_list.remove(j)

print("deleting " + str(len(duplicates)) + " files in " + root_dir)

for item in duplicates:
    os.remove(item)

print("done")



