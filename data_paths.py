import glob
import os
import iris
import numpy as np

from varname_dictionary import varname_dictionary

# Use this command to import the dictionary
# from data_paths import filepath_dict
# Then paths can be accessed via filepath_dict[factor used]

filepath_dict = {
1:"/jasmin/users/bakera/CMSS17/ctl/{}/{}/xmrai/",
2:"/jasmin/users/ncastr25/xonma/{}/{}/xonma/",
0.75:"/jasmin/users/ncastr12/xonxa/{}/{}/xonxa/",
0.5:"/jasmin/users/ncastr17/xonia/{}/{}/xonia/",
0.25:"/jasmin/users/ncastr13/xoncc/{}/{}/xoncc/",
0:"/jasmin/users/ncastr10/xonta/{}/{}/xonta/",
}

def in_any_of_strings(string, liststrings):
    return np.any([string in l for l in liststrings])

def varname_search(variable, filepath):
    lkey = [key for key, value in varname_dictionary.iteritems() if value[0] == variable]
    
    codes = [l for l in lkey if in_any_of_strings(l, glob.glob(filepath+"*"))]
    if len(codes)==0:
        raise ValueError("No codes found for variable name {}".format(variable))
    elif len(codes)>1:
        raise ValueError("Too many codes ({}) found for variable name {}".format(len(codes), variable))
    return codes[0]

def load_cubes(factors, subfile='annual', variable = "air_temperature"):
    """
    Function to load in cubes of one variable type for one or more factors.
    eg usage
        cubes = load_cubes([1, 2], subfile='annual', variable = "air_temperature")
        cubes = load_cubes([0.5, 1], subfile='seasonal', variable = "soil_respiration_carbon_flux")
        
    returns a list of iris cubes
    """
    cubes = []
    for f in factors:
        print('loading - factor {} - {} -  variable - {}'.format(f, subfile, variable))
        rootpath = filepath_dict[f]
        
        fullpath = rootpath.format(subfile, variable)
        fullpath = fullpath + "*{}*".format(varname_search(variable, fullpath))
        print(fullpath)
        cube = iris.load(fullpath)
        cubes.append(cube.concatenate()[0])
    print('loaded')
    return cubes


