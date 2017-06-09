import pandas as pd
import numpy as np
import json
import sys
from tqdm import tqdm

interColor = { "Aromatic stacking": "#E36262","Hydrogen bond": "#02B7DB","Hydrophobic": "#F0ED67","Repulsive": "#512B8B","Salt bridge": "#519136" }

cinema = { "H": "#1240AB","K": "#1240AB","R": "#1240AB","D": "#BF3030","E": "#BF3030","N": "#9F3ED5","Q": "#9F3ED5","S": "#9F3ED5", "T": "#9F3ED5",
"A": "#4EA429","G": "#4EA429","I": "#4EA429","L": "#4EA429","M": "#4EA429","V": "#4EA429","F": "#009999","P": "#009999","W": "#009999","Y": "#009999",
"C": "#FFAA00",}

clustal = { "G": "#FF9640","P": "#FF9640","S": "#FF9640","T": "#FF9640","H": "#BF3030","K": "#BF3030","R": "#BF3030","F": "#1240AB", "W": "#1240AB",
"Y": "#1240AB","I": "#008500","L": "#008500","M": "#008500","V": "#008500",}

lesk = { "A": "#FF9640","G": "#FF9640","S": "#FF9640","T": "#FF9640","C": "#269926","F": "#269926","I": "#269926","L": "#269926", "M": "#269926",
"P": "#269926","V": "#269926","W": "#269926","Y": "#269926","H": "#CD0077","N": "#CD0077","Q": "#CD0077","D": "#BF3030","E": "#BF3030","K": "#1240AB",
"R": "#1240AB",}

# Achar o index de um item em uma lista

def indexinList(list, name):
    for i in range(len(list)):
        if list[i]['name'] == name:
            index = i
            return index
            break

def findCinemaColor(name):
    try:
        vec = name.split("_")[3];
        return cinema.values()[cinema.keys().index(vec[0])]
    except Exception as e:
        return "#ccc"

def findLeskColor(name):
    try:
        vec = name.split("_")[3];
        return cinema.values()[lesk.keys().index(vec[0])]
    except Exception as e:
        return "#ccc"

def findClustalColor(name):
    try:
        vec = name.split("_")[3];
        return clustal.values()[clustal.keys().index(vec[0])]
    except Exception as e:
        return "#ccc"

def findlinkcolor(name):
    return interColor.values()[interColor.keys().index(name.strip())]

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
for index, row in tqdm(csvdf.iterrows(),desc='GET THE NODES'):
    obj = {};obj2 = {}
    if(row['interaction'] != ""):
        if(row['atom1'] != row['atom2']):
            obj['name'] = row['atom1']
            obj['cinema'] = findCinemaColor(obj['name'])
            obj['clustal'] = findClustalColor(obj['name'])
            obj['lesk'] = findLeskColor(obj['name'])
            nodes.append(obj)
            obj2['name'] = row['atom2']
            obj2['cinema'] = findCinemaColor(obj2['name'])
            obj2['clustal'] = findClustalColor(obj2['name'])
            obj2['lesk'] = findLeskColor(obj2['name'])
            nodes.append(obj2)
            groups.append(row['atom1'].split("_")[3] + row['atom1'].split("_")[4])
            groups.append(row['atom2'].split("_")[3] + row['atom2'].split("_")[4])


groups = np.unique(groups).tolist()

# Group the nodes
for node in tqdm(nodes,desc='GROUP THE NODES'):
    stringid = node['name'].split("_")[4]
    residue =  node['name'].split("_")[3]
    stringroup = residue + stringid
    node['group'] = groups.index(stringroup)

nodes = np.unique(nodes).tolist()


# Get the links
for index, row in tqdm(csvdf.iterrows(),desc='GET THE LINKS'):
    link = {}
    if(row['interaction'] != ""):
        if(row['atom1'] != row['atom2']):
            link['source'] = indexinList(nodes,row['atom1'])
            link['target'] = indexinList(nodes,row['atom2'])
            link['color'] = findlinkcolor(row['interaction'])
            link["type"] = row['interaction']
            links.append(link)


graph = {}
graph['links']= links
graph['nodes'] = nodes


with open("graph2.json", 'w') as outfile:
    json.dump(graph,outfile)
