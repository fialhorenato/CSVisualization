import pandas as pd
import numpy as np
import json
import sys
from array import array

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

def getIndexOfNodes(l, index, value):
    for pos,t in enumerate(l):
        if t[index] == value:
            return pos


# Creates 2 ndarrays to get the nodes and the links
nodes = []
links = []

# Iterate on the dataframe got from the .csv file
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        obj = {}; obj2 ={}
        obj['name'] = string
        nodes.append(obj)
        obj2['name'] = string2
        nodes.append(obj2)

# Get only the unique nodes
nodes =  np.unique(nodes)



# Get the correct links with the index after the pre-processing
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        link = {};obj1 = {};obj2 = {};
        obj1['name'] = correctString(row['atom1'])
        obj2['name'] = correctString(row['atom2'])
        index1 = nodes.tolist().index(obj1)
        index2 = nodes.tolist().index(obj2)
        link["source"] = index1
        link["target"] = index2
        link["weight"] = round(row['distance'])
        link["type"] = row['interaction']
        links.append(link)

# Get only the unique links
links =  np.unique(links)

linksdf = pd.DataFrame.from_dict(links, orient='columns')
nodesdf = pd.DataFrame.from_dict(nodes, orient='columns')

graph = {}
graph['links']= links.tolist()
graph['nodes'] = nodes.tolist()

with open("graph.json", 'w') as outfile:
    json.dump(graph,outfile)
