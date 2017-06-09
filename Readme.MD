# VERMONT (ViewER MutatiON) 2.0

This is a project made for the [LBS](http://www.lbs.dcc.ufmg.br/) as an upgrade from the old VERMONT data visualization using new tools, techniques and technology.

This project a data visualization of the protein ligands using a force-based layout.

The data analysis from the given .csv file and generation of the json file that is consumed by the visualization uses Python and Pandas.

The data visualization uses d3.js and 3DMol.

## INSTALL

### Ubuntu

```Shell Session
sudo apt-get install python-virtualenv
sudo apt-get install python-dev
sudo apt-get install build-essential
```

### Then

```Shell Session
virtualenv NAMEOFYOURVENV
source NAMEOFYOURVENV/bin/activate
sudo pip install -r requirements.txt
```

## REQUIREMENTS

```Shell Session
pandas
tqdm
```

## CSV TEMPLATE EXAMPLE

```Shell Session
atom1,type_atom1,atom2,type_atom2,distance,interaction
ATOM A,Hydrophobic,ATOM B,Hydrophobic/Aromatic,3.83218906109811,Hydrophobic
ATOM C,Hydrophobic/Aromatic,ATOM D,Hydrophobic/Aromatic,4.44219832965617,Aromatic stacking
```

If you have any questions about the CSV files, feel free to contact me.

## CONTRIBUTING

The project right now is deprecated and with no further development.

Any questions or issues, feel free to contact me or open an issue in this project.

## RUN

``python generator2.py file.csv``
