import utm
import csv
import pandas
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, Delaunay
import networkx as nx
import folium
from folium import plugins


path_to_dataset = '../data/Sydney_Basin/'
path_to_output = '../data/'

zone_number = 55
zone_letter = "H"
utm_list = []
points_utm_list = 0
points = []


def concave(points,alpha_x=150,alpha_y=250):
    points = [(i[0],i[1]) if type(i) != tuple else i for i in points]
    de = Delaunay(points)
    dec = []
    a = alpha_x
    b = alpha_y
    for i in de.simplices:
        tmp = []
        j = [points[c] for c in i]
        if abs(j[0][1] - j[1][1])>a or abs(j[1][1]-j[2][1])>a or abs(j[0][1]-j[2][1])>a or abs(j[0][0]-j[1][0])>b or abs(j[1][0]-j[2][0])>b or abs(j[0][0]-j[2][0])>b:
            continue
        for c in i:
            tmp.append(points[c])
        dec.append(tmp)
    G = nx.Graph()
    for i in dec:
            G.add_edge(i[0], i[1])
            G.add_edge(i[0], i[2])
            G.add_edge(i[1], i[2])
    ret = []
    for graph in nx.connected_component_subgraphs(G):
        ch = ConvexHull(graph.nodes())
        tmp = []
        for i in ch.simplices:
            tmp.append(graph.nodes()[i[0]])
            tmp.append(graph.nodes()[i[1]])
        ret.append(tmp)
    return ret

def process(path_to_dataset, path_to_output, zone_number, zone_letter):
    data_file_name = 'KATSF.csv'
    data_file_output = 'Output_' + data_file_name

    with open(path_to_dataset + data_file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        data_list = list(reader)
        xyz_columns = []

        ##case 1
        firstRow = data_list[0]
        if "NAME" in firstRow:
            x_coorindate = 0
            y_coorindate = 0
            z_coorindate = 0
            for row in data_list:
                xyz_columns = row[2:]
                try:
                    x_coorindate = float(row[2])
                    y_coorindate = float(row[3])
                    z_coorindate = float(row[4])
                    utm_tuple= list(utm.to_latlon(x_coorindate, y_coorindate, zone_number, zone_letter))
                    utm_tuple.append(z_coorindate)
                    utm_list.append(utm_tuple)
                except:
                    pass
        else:
        ##case 2
            counter = 0
            for index, row in enumerate(data_list):
                counter +=1
                if "X" and "Y" and "Z" in data_list[index]:
                    xyz_columns = data_list[12:]
            #convert csv to latlon
            for point in xyz_columns:
                x_coorindate = float(point[0])
                y_coorindate = float(point[1])
                z_coorindate = float(point[2])

                ##remove null points if they are 99999.00
                if z_coorindate != 99999.00:
                    utm_tuple= list(utm.to_latlon(x_coorindate, y_coorindate, zone_number, zone_letter))
                    utm_tuple.append(z_coorindate)
                    utm_list.append(utm_tuple)
            length_utm_list = len(utm_list)
    ##write and create cvs file
    writer = csv.writer(open(path_to_output + data_file_output, 'w'))
    for point in utm_list:
        writer.writerow(point)


process(path_to_dataset, path_to_output, zone_number, zone_letter)
#
points_utm_list = len(utm_list)
from folium.plugins import HeatMap

def folium_heatmap(utm_list):
    lats = [float(item[0]) for item in utm_list]
    longs = [float(item[1]) for item in utm_list]
    mag = [float(item[2]) for item in utm_list]
    terrain_map = folium.Map(location=[-33.868819700, 151.209295500], tiles='Stamen Terrain', zoom_start=6)
    HeatMap(zip(lats, longs, mag), radius = 10).add_to(terrain_map)
    # heat_map.add_children(plugins.Heatmap(zip(lats, longs, mag), radius = 10))
    terrain_map.save('../code/new.html')

# folium_heatmap(utm_list)

# def convex_hull(utm_list):
#     ##Only output latitude and longitude from the utm_list
#     for item in utm_list:
#         points.append(item[:2])
#     hull = ConvexHull(points)
#     plot_convex_hull(points, hull)
#
# def plot_convex_hull(points, hull):
#     points = array(points)
#     latitude = points[:,0]
#     longitude = points[:,1]
#     plt.plot(latitude, longitude, 'o')
#
#     for simplex in hull.simplices:
#         plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
#     plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
#     plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
#     plt.show()
#
# convex_hull(utm_list)
#
# def plot_concave_hull(points):
#     points = array(points)
#     latitude = points[:,0]
#     longitude = points[:,1]
#     plt.plot(*zip(*points), marker='o', color='g')
#     plt.show()

# plot_concave_hull(points)
