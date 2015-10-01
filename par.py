import pandas as pd
import numpy as np

dic =  pd.read_csv('1BGA.interaction.csv',keep_default_na=False,na_values=[" "])

class Link(object):
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

def correctString(string):
    vector = string.split("_")
    result = vector[3] + vector[4]
    return result

atoms = []
links = []

for index, row in dic.iterrows():
    if(row['interaction'] != ""):
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        atoms.append(string)
        atoms.append(string2)

atoms =  np.unique(atoms)

# Is not working properly

for index, row in dic.iterrows():
    if(row['interaction'] != ""):
        string = correctString(row['atom1'])
        string2 = correctString(row['atom2'])
        index1 = atoms.tolist().index(string)
        index2 = atoms.tolist().index(string2)
        link = Link(index1, index2)
        links.append(link)
