from scipy.spatial import cKDTree
import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull, Delaunay
import folium
from folium import plugins 
from folium.plugins import HeatMap

def read_data(input_filename):
    """Read in a file, returning an array and a kdtree"""
    with open(input_filename) as input_file:
        input_reader = csv.reader(input_file)
        data_points = np.array([tuple(map(float,line)) for line in input_reader])
        kdtree = cKDTree(data_points[:,[0,1]])
    return (data_points, kdtree)

def create_kdtree(data_points):
    return (data_points, cKDTree(data_points[:,[0,1]]))

def bounds(kdtree):
    """Return the bounds of a kdtree"""
    return (tuple(kdtree.mins), tuple(kdtree.maxes))

def query(data_points, kdtree, queries, resolution):
    """Given the data, a kdtree, a list of points and
    a radius to search in, return a value for each point"""
    return [point_value(data_points[x][:,[2]],data_points,queries[n],kdtree)
            for n,x in enumerate(kdtree.query_ball_point(queries,r=resolution))]

def point_value(arr,data_points,x,kdtree):
    """Get the mean value of a set of points returned from
    a ball query on the kdtree. If there are no points in the radius,
    just return the closest"""
    if len(arr) == 0: return data_points[kdtree.query(x)[1]][2]
    return np.mean(arr)

def grid(data_points, kdtree, xbounds, ybounds, num_xsteps=300, num_ysteps=300):
    """Return a grid of z value between the bounds given. It'll work for
    things that aren't square, but please try and make it a square"""
    (minx, maxx) = xbounds
    (miny, maxy) = ybounds
    res = np.zeros((num_xsteps,num_ysteps))
    xsteps = np.linspace(minx,maxx,num_xsteps)
    ysteps = np.linspace(miny,maxy,num_ysteps)
    for (i,x) in enumerate(xsteps):
        for (j,y) in enumerate(ysteps):
            res[(i,j)] = query(data_points, kdtree, [(x,y)], max((maxx-minx)/num_xsteps,(maxy-miny)/num_ysteps))[0]
    return (xsteps,ysteps,res)

def draw(xs,ys,zs):
    """Draw a mesh from a grid of points
    :param xs: A 1-D array of x-coordinates
    :param ys: A 1-D array of y-cooridinates
    :param zs: A 2-D array of heights"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    xs,ys = np.meshgrid(xs,ys)
    ax.plot_surface(xs,ys,zs)
    plt.show()

def downscale(data_points, kdtree, xbounds, ybounds, num_xsteps=300, num_ysteps=300):
    """Make a new dataset at a lower resolution. This won't interpolate to create
    new points, so it can't be used to increase resolution
    :param data_points: An array of x,y,z values
    :param kdtree: The matching tree
    """
    (xs,ys,data) = grid(data_points, kdtree, xbounds, ybounds, num_xsteps, num_ysteps)
    (xs,ys) = np.meshgrid(xs,ys)
    xs = xs.flatten()
    ys = ys.flatten()
    data = data.flatten()
    new_data = np.array(xs,ys,data).T
    return (new_data, cKDTree(new_data[:,[0,1]]))

def merge(old_data_points, new_data_points):
    """Merge two sets of data. The first one must be larger
    :param old_data_points: The "base" dataset
    :param new_data_points: The new data
    :returns: A pair containing an array for all the data, and the corresponding kd-tree"""
    hull = Delaunay(new_data_points[:,[1,2]])
    smaller = np.array(old_data_points[hull.find_simplex(old_data_points[:,[0,1]]) < 0])
    merged_data = np.concatenate((new_data_points, smaller))
    return create_kdtree(merged_data)

def read_tiered_data(filenames):
    """Given a list of files partially ordered by resolution
    (low to high) return a kdtree and dataset
    :param filenames: A list of filenames
    :returns: A pair containing an array for all the data, and the corresponding kd-tree
    """
    initial = None
    kdtree = None
    for f in filenames:
        if kdtree is None:
            initial,kdtree = read_data(f)
        else:
            (d,t) = read_data(f)
            (initial,kdtree) = merge(initial,d)
    return (initial, kdtree)

def draw_heatmap(x,y,z):
    """Draw a heatmap using folium. Not really that useful"""
    x,y = np.meshgrid(x,y)
    terrain_map = folium.Map(location=[x[0,0], y[0,0]], tiles='Stamen Terrain', zoom_start=12)
    HeatMap(zip(x.flatten(),y.flatten(),z.flatten()), radius=10).add_to(terrain_map) 
    terrain_map.save('map.html')
