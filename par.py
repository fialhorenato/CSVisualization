import pandas as pd
import numpy as np
import json
import sys

# Get the parameters
params = sys.argv
# Open the csv file using pandas
if  (len(params) > 1 and params[1] != ''):
    csvdf =  pd.read_csv(params[1],keep_default_na=False,na_values=[" "])
else:
    csvdf =  pd.read_csv('teste.csv',keep_default_na=False,na_values=[" "])

# Takes this string as example (ATOM_1_N_THR_2_A,) and got only the residue (THR2)
def correctString(string):
    vector = string.split("_")
    result = vector[3] + vector[4]
    return result

# Save a ndarray to a json file , nd = ndarray, jsonfile = 'file.json'
def ndarray_to_json(nd , jsonfile):
    with open(jsonfile, 'w') as outfile:
        json.dump(pd.DataFrame.to_json(pd.DataFrame(nd),orient='index'), outfile)


# Creates 2 ndarrays to get the nodes and the links
nodes = []
links = []

# Iterate on the dataframe got from the .csv file
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        nodes.append(string)
        nodes.append(string2)

# Get only the unique nodes
nodes =  np.unique(nodes)

# Get the correct links with the index after the pre-processing
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        link = {}
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        index1 = nodes.tolist().index(string)
        index2 = nodes.tolist().index(string2)
        link["x"] = index1
        link["y"] = index2
        links.append(link)

# Get only the unique links
links =  np.unique(links)

ndarray_to_json(nodes,'nodes.json')
ndarray_to_json(links,'links.json')
