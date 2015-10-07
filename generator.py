import pandas as pd
import numpy as np
import json
import sys
from array import array

#Define the colors for the links
interColor = { "Aromatic stacking": "#E36262","Hydrogen bond": "#02B7DB","Hydrophobic": "#F0ED67","Repulsive": "#512B8B","Salt bridge": "#519136" }
cinema = { "H": "#1240AB","K": "#1240AB","R": "#1240AB","D": "#BF3030","E": "#BF3030","N": "#9F3ED5","Q": "#9F3ED5","S": "#9F3ED5", "T": "#9F3ED5",
"A": "#4EA429","G": "#4EA429","I": "#4EA429","L": "#4EA429","M": "#4EA429","V": "#4EA429","F": "#009999","P": "#009999","W": "#009999","Y": "#009999",
"C": "#FFAA00",}
#clustal = { "Aromatic stacking": "#E36262","Hydrogen bond": "#02B7DB","Hydrophobic": "#F0ED67","Repulsive": "#512B8B","Salt bridge": "#519136" }
#lesk = { "Aromatic stacking": "#E36262","Hydrogen bond": "#02B7DB","Hydrophobic": "#F0ED67","Repulsive": "#512B8B","Salt bridge": "#519136" }

def indexinList(List, obj):
    for i in range(len(List)):
        if List[i]['name'] == obj['name'] and List[i]['type'] == obj['type'] :
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
        obj['type'] = row['type_atom1']
        obj['cinema_color'] = cinema.values()[cinema.keys().index(string[0])]
        #obj['clustal_color'] =
        #obj['lesk_color'] =
        nodes.append(obj)
        obj2['cinema_color'] = cinema.values()[cinema.keys().index(string2[0])]
        obj2['type'] = row['type_atom2']
        obj2['name'] = string2
        nodes.append(obj2)

# Get only the unique nodes
nodes =  np.unique(nodes)
print nodes
# Get the correct links with the index after the pre-processing
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        link = {};obj1 = {};obj2 = {};
        obj1['name'] = correctString(row['atom1'])
        obj1['type'] = row['type_atom1']
        obj2['name'] = correctString(row['atom2'])
        obj2['type'] = row['type_atom2']
        #index1 = nodes.tolist().index(obj1)
        index1 = indexinList(nodes.tolist(),obj1)
        index2 = indexinList(nodes.tolist(),obj2)
        link["source"] = index1
        link["target"] = index2
        link["distance"] = row['distance']
        link["value"] = round(row['distance'])
        link["type"] = row['interaction']
        link["color"] = interColor.values()[interColor.keys().index(row['interaction'].strip())]
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
