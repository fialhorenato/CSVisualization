import pandas as pd
import numpy as np
import json
import sys

# Achar o index de um item em uma lista

def indexinList(list, name):
    for i in range(len(list)):
        if list[i]['name'] == name:
            index = i
            return index
            break

# Get the parameters
params = sys.argv
# Open the csv file using pandas
if  (len(params) > 1 and params[1] != ''):
    csvdf =  pd.read_csv(params[1],keep_default_na=False,na_values=[" "])
else:
    csvdf =  pd.read_csv('teste.csv',keep_default_na=False,na_values=[" "])

nodes = []
groups = []
links = []

# Get the nodes
for index, row in csvdf.iterrows():
    obj = {};obj2 = {}
    if(row['interaction'] != ""):
        if(row['atom1'] != row['atom2']):
            obj['name'] = row['atom1']
            nodes.append(obj)
            obj2['name'] = row['atom2']
            nodes.append(obj2)
            groups.append(row['atom1'].split("_")[3] + row['atom1'].split("_")[4])
            groups.append(row['atom2'].split("_")[3] + row['atom2'].split("_")[4])


groups = np.unique(groups).tolist()

# Group the nodes
for node in nodes:
    stringid = node['name'].split("_")[4]
    residue =  node['name'].split("_")[3]
    stringroup = residue + stringid
    node['group'] = groups.index(stringroup)

nodes = np.unique(nodes).tolist()


# Get the links
for index, row in csvdf.iterrows():
    link = {}
    if(row['interaction'] != ""):
        if(row['atom1'] != row['atom2']):
            link['source'] = indexinList(nodes,row['atom1'])
            link['target'] = indexinList(nodes,row['atom2'])
            links.append(link)


graph = {}
graph['links']= links
graph['nodes'] = nodes


with open("graph2.json", 'w') as outfile:
    json.dump(graph,outfile)
