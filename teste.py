import os 
  
# Directory 
directory = "GeeksforGeeks"
  
# Parent Directory path 
parent_dir = "C:/Users/alex.soares3/Documents/GitHub/tocadiscos"
  
# Path 
path = os.path.join(parent_dir, directory) 
  
# Create the directory 
# 'GeeksForGeeks' in 
# '/home / User / Documents' 
os.mkdir(path) 
print("Directory '% s' created" % directory) 