import pandas as pd
import numpy as np
import json

# Open the csv file using pandas
csvdf =  pd.read_csv('teste.csv',keep_default_na=False,na_values=[" "])

# Takes this string as example (ATOM_1_N_THR_2_A,) and got only the residue (THR2)
def correctString(string):
    vector = string.split("_")
    result = vector[3] + vector[4]
    return result

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

# Transforms both dataframes (nodes and links) to JSON
Json1 = pd.DataFrame.to_json(pd.DataFrame(nodes),orient='index')
Json2 = pd.DataFrame.to_json(pd.DataFrame(links), orient='index')

# Save those links to .json files
with open('nodes.json', 'w') as outfile:
    json.dump(Json1, outfile)

with open('links.json', 'w') as outfile:
    json.dump(Json2, outfile)
