# ===================
# famous_utilities.py
# ===================
# Miscellaneous functions for working with iris cubes and FAMOUS output.
# CMSS2017, Cambridge.

import numpy as np


# Add coords to time dimension to allow aggregation
def add_time_coords(cube):
    import iris.coord_categorisation
    time_cf_standard_name = 'time'
    iris.coord_categorisation.add_month_number(cube,time_cf_standard_name)
    iris.coord_categorisation.add_season(cube,time_cf_standard_name)
    iris.coord_categorisation.add_season_year(cube,time_cf_standard_name)
    iris.coord_categorisation.add_year(cube,time_cf_standard_name)
    return cube

# Concatenate cube list of year files and add coords needed for seasonal aggregation and/or extraction
def process_cubelist(cubelist):
    import iris.coord_categorisation
    import iris.experimental.equalise_cubes
    iris.experimental.equalise_cubes.equalise_attributes(cubelist)
    cube = cubelist.concatenate()[0]
    add_time_coords(cube)
    return cube

# Convert precipitation flux to mm/day
def convert_precip_flux_units(cube):
    cube.data = cube.data * 86400.
    cube.units = 'mm/day'
    return cube

# Convert specific humidity to g/kg
def convert_q_units(cube):
    cube.data = cube.data * 1000.
    cube.units = 'g/kg'
    return cube

# Compute mean of iris.cube.CubeList()
def cubelist_mean(cubelist):
    import iris.analysis.maths
    n = float(len(cubelist))
    mean_cube = reduce(iris.analysis.maths.add,cubelist) / n
    return mean_cube

# Make pressure coord points integers
def format_pressure_levels(cube):
    cube.coord('pressure').points = cube.coord('pressure').points.astype(int).tolist()
    return cube

# Find nearest value in array
def find_nearest(array,value):
    idx = (abs(array-value)).argmin()
    return array[idx]

# Find approximate sigma level corresponding to given pressure level
def approximate_sigma_level(p_lev,cube):
    global_mean_surface_pressure = 1013.    #hPa
    ratio = float(p_lev)/global_mean_surface_pressure
    sigma_level = find_nearest(cube.coord('sigma').points,ratio)
    return sigma_level

# Find model level corresponding to given sigma level
def get_model_level(sigma,cube):
    model_levels = cube.coord('model_level_number').points
    m_lev = model_levels[np.where(cube.coord('sigma').points == sigma)[0][0]]
    return m_lev

def famous_p_levs():
    return [10.,30.,50.,100.,150.,200.,250.,300.,
            400.,500.,600.,700.,850.,950.,1000.]


if __name__ == '__main__':
    pass

# END
