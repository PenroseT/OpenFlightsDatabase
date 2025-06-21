import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, LineString, MultiLineString
import inspect
import sqlite3

R_earth = 6378 # The radius of Earth 

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

def dict_factory(cursor, row):
    # Used to fetch the results in the form of a dictionary
    # so that it is easier to access data
    return {column[0]: row[idx] for idx, column in enumerate(cursor.description)}

def create_path(lonp1, latp1, lonp2, latp2):
    # Creates a single or two linestrings from lon/lat coordinates
    # of two endpoints defining the route

    l = np.abs(lonp2-lonp1)

    if l<=180.0:
        return LineString([(lonp1, latp1), (lonp2, latp2)])
    else:
        # The latitude of the route line at the international date line:
        y_bound = idl_latitude(lonp1, latp1, lonp2, latp2)
        if lonp2>lonp1:
            # P1 is close to the left boundary and P2 to the right boundary
            return MultiLineString([[(lonp1, latp1), (-180.0, y_bound)],
                                    [(lonp2, latp2), (180.0, y_bound)]])
        elif lonp1>lonp2:
            return MultiLineString([[(lonp1, latp1), (180.0, y_bound)],
                                    [(lonp2, latp2), (-180.0, y_bound)]])

def idl_latitude(lonp1, latp1, lonp2, latp2):
    # An elementary geometrical calculation determines the latitude
    # of the straight line connecting two points and crossing the 
    # international date line

    if lonp2>lonp1:
        return latp2+((latp2-latp1)*(180-lonp2))/(lonp2-lonp1-360)
        
    elif lonp1>lonp2:
        return latp1+((latp1-latp2)*(180-lonp1))/(lonp1-lonp2-360)

def create_path_pt(point1, point2):
    # Creates a single or two linestrings from two points
    # defined as a (lon, lat) coordinate tuple
    
    l = np.abs(point1[0]-point2[0])
    
    if l<=180.0:
        return LineString([point1, point2])
    else:
        # The left point is the point with smaller longitude
        if point2[0]>point1[0]:
            left_point = point1
            right_point = point2
        else:
            left_point = point2
            right_point = point1
        # The latitude of the route line at the international date line:
        y_bound = idl_latitude_pt(left_point, right_point)
        # left_point is close to the left boundary and right_point to the right boundary
        return MultiLineString([[left_point, (-180.0, y_bound)],
                                    [right_point, (180.0, y_bound)]])

def idl_latitude_pt(left_point, right_point):
    # The date line route latitude for two connected points
    lonp1, latp1 = left_point
    lonp2, latp2 = right_point
    
    return latp2+((latp2-latp1)*(180-lonp2))/(lonp2-lonp1-360)


def haversine(x):
    return 0.5*(1-np.cos(x))

def haversine_distance(lon1, lat1, lon2, lat2):
    # Calculates the distance between two points on the Earth's
    # surface using the haversine formula

    delta_phi = np.radians(lon2-lon1)
    delta_lam = np.radians(lat2-lat1)
    phi_m = np.radians(0.5*(lon1+lon2))
    
    return 2*R_earth*np.arcsin(np.sqrt(haversine(delta_phi)+\
                               haversine(delta_lam)*(1-haversine(delta_phi)\
                               -haversine(2*phi_m))))

def create_world():
    shp = "maps/110m_cultural/ne_110m_admin_0_countries.shp"
    world = gpd.read_file(shp)
    return world


def perform_query(database, query, functions, params):

    con = sqlite3.connect("openflights.db")
    con.row_factory = dict_factory

    for func in functions:
        # Count the number of arguments
        sig = inspect.signature(func)
        argnum = len(sig.parameters)
        # Registers the function as py_function_name
        con.create_function("py_"+func.__name__, argnum, func)

    cur = con.cursor()
    cur.execute(query, params)
    result = cur.fetchall()
    con.close()
    
    return result

    
def create_routes(database, query, functions, params):
    # The query is constructed so that the objects have the following information
    # source and destination names as src_nm and dst_nm,
    # the coordinates of the source and destination airports
    
    result = perform_query(database, query, functions, params)

    route_names = []
    route_lines = []

    # Lines that connect selected cities
    for route in result:
        route_line = create_path_pt((route['src_lon'], route['src_lat']),
                                 (route['dst_lon'], route['dst_lat']))
        route_name = f"{route['src_nm']}"+'-'+f"{route['dst_nm']}" # Route is specified in the form 'SRC-DST'
        route_lines.append(route_line)
        route_names.append(route_name)

    # Dataframe with column route that contains the name of the column
    # and column geometry that contains coordinates of the LineString endpoints.
    # The 'crs' specifies the coordinate system.
    gdf_route = gpd.GeoDataFrame({'route': route_names,
                                  'geometry': route_lines},
                                   crs='EPSG:4326')

    return gdf_route

def create_airports(database, query, functions, params):
    # The query is constructed so that the objects have the following information
    # airport name as airport_nm,
    # the coordinates of the airport
    # magnitude of the airport as airport_size 

    result = perform_query(database, query, functions, params)
    
    airport_names = []
    airports = []
    airport_sizes = []

    for _airport in result:
        airport = Point(_airport['airport_lon'], _airport['airport_lat'])
        airport_name = f"{_airport['airport_nm']}" 
        airport_size = int(_airport['airport_size'])
        airport_names.append(airport_name)
        airports.append(airport)
        airport_sizes.append(airport_size)
    
    gdf_airports = gpd.GeoDataFrame({'airport': airport_names,
                                  'airport_sizes': airport_sizes,
                                  'geometry': airports},
                                   crs='EPSG:4326')

    return gdf_airports

def populated_world(world, axis, cmap='OrRd', linewidth=0.4, alpha=0.9,
                    legend_loc='lower left', legend_fontsize=15,
                    legend_title_fontsize=20):

    bins = [2.5e6, 7e6, 15e6, 40e6, max(world['POP_EST'])]

    # Plot the world map
    ax = world.plot(column='POP_EST', cmap=cmap,
           scheme='user_defined', classification_kwds=dict(bins=bins),
           edgecolor='white', linewidth=linewidth, alpha=alpha,
           legend=True, legend_kwds={'loc':legend_loc ,'fontsize':legend_fontsize, 'title_fontsize':legend_title_fontsize},
           ax=axis)

    custom_labels = ['< 2.5M',
                    '2.5M–7M',
                    '7M–15M',
                    '15M–40M',
                    '> 40M']

    # Grab the Legend instance
    leg = ax.get_legend()
    leg.set(title="Population")

    # Replace each text
    for text, new_label in zip(leg.get_texts(), custom_labels):
        text.set_text(new_label)


def route_name_identifier(name):
    # Takes two airport ids and assigns a unique identifier LOC1-LOC2
    # that creates an equivalence between flights going from
    # point1 to point2 and from point2 to point1
    
    names_sorted = sorted(name.split('-'))
    
    return names_sorted[0]+'-'+names_sorted[1]

def route_identifier(id1, id2):
    # Takes two airport numerical ids and assigns a unique identifier
    
    ids_sorted = sorted([id1, id2])
    id_string = ''.join(str(_id) for _id in ids_sorted)
    
    return int(id_string)