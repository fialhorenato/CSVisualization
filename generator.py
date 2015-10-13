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
clustal = { "G": "#FF9640","P": "#FF9640","S": "#FF9640","T": "#FF9640","H": "#BF3030","K": "#BF3030","R": "#BF3030","F": "#1240AB", "W": "#1240AB",
"Y": "#1240AB","I": "#008500","L": "#008500","M": "#008500","V": "#008500",}

lesk = { "A": "#FF9640","G": "#FF9640","S": "#FF9640","T": "#FF9640","C": "#269926","F": "#269926","I": "#269926","L": "#269926", "M": "#269926",
"P": "#269926","V": "#269926","W": "#269926","Y": "#269926","H": "#CD0077","N": "#CD0077","Q": "#CD0077","D": "#BF3030","E": "#BF3030","K": "#1240AB",
"R": "#1240AB",}

def indexinList(List, obj):
    for i in range(len(List)):
        if List[i]['name'] == obj['name'] :
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
nodesteste = []
linksteste = []

# Iterate on the dataframe got from the .csv file
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        if (string != string2) :

            obj = {}; obj2 ={}
            obj['name'] = string
            #obj['type'] = row['type_atom1']

            try:
                obj['cinema_color'] = cinema.values()[cinema.keys().index(string[0])]
            except Exception as e:
                obj['cinema_color'] = "#ccc"

            try:
                obj['clustal_color'] = clustal.values()[clustal.keys().index(string[0])]
            except Exception as e:
                obj['clustal_color'] = "#ccc"

            try:
                obj['lesk_color'] = lesk.values()[lesk.keys().index(string[0])]
            except Exception as e:
                obj['lesk_color'] = "#ccc"

            nodes.append(obj)
            try:
                obj2['cinema_color'] = cinema.values()[cinema.keys().index(string2[0])]
            except Exception as e:
                obj2['cinema_color'] = "#ccc"
            try:
                obj2['clustal_color'] = clustal.values()[clustal.keys().index(string2[0])]
            except Exception as e:
                obj2['clustal_color'] = "#ccc"
            try:
                obj2['lesk_color'] = lesk.values()[lesk.keys().index(string2[0])]
            except Exception as e:
                obj2['lesk_color'] = "#ccc"

            #obj2['type'] = row['type_atom2']
            obj2['name'] = string2
            nodes.append(obj2)
            nodesteste.append(string)
            nodesteste.append(string2)

# Get only the unique nodes
nodes =  np.unique(nodes)

# Search how many of each node have
for node in nodes:
    node['value'] = (nodesteste.count(node['name']))

# Get the correct links with the index after the pre-processing
for index, row in csvdf.iterrows():
    if(row['interaction'] != ""):
        link = {};obj1 = {};obj2 = {};srcobj={};
        if (correctString(row['atom1']) != correctString(row['atom2'])):
            obj1['name'] = correctString(row['atom1'])
            obj1['type'] = row['type_atom1']
            obj2['name'] = correctString(row['atom2'])
            obj2['type'] = row['type_atom2']
            index1 = indexinList(nodes.tolist(),obj1)
            index2 = indexinList(nodes.tolist(),obj2)
            link["source"] = index1
            link["target"] = index2
            link["distance"] = row['distance']
            link["type"] = row['interaction']
            link["color"] = interColor.values()[interColor.keys().index(row['interaction'].strip())]
            links.append(link)
            srcobj['source'] = index1
            srcobj['target'] = index2
            linksteste.append(srcobj)


# Get only the unique links
links =  np.unique(links)

# Search how many of each links have
for link in links:
    srchobj = {}
    srchobj['source'] = link['source']
    srchobj['target'] = link['target']
    link['value'] = (linksteste.count(srchobj))

linksdf = pd.DataFrame.from_dict(links, orient='columns')
nodesdf = pd.DataFrame.from_dict(nodes, orient='columns')

graph = {}
graph['links']= links.tolist()
graph['nodes'] = nodes.tolist()

with open("graph.json", 'w') as outfile:
    json.dump(graph,outfile)
