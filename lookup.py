import re
import requests
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

MAX_MARKER_SIZE = 150
MIN_MARKER_SIZE = 3

ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

ip_occurrence = {}

def get_ip_addresses():
    fil = open("auth.log", "r")
    for line in fil.readlines():
        match_obj = re.search(ip_regex, line)
        if(match_obj):
            ip = match_obj.group()
            if ip in ip_occurrence:
                ip_occurrence[ip]['occurrence'] += 1
            else:
                ip_occurrence[ip] = {'occurrence': 1}

def get_locations():
    for ip_address in ip_occurrence:
        location = requests.get('http://ipinfo.io/'+ip_address).json()
        location.pop('ip')
        ip_occurrence[ip_address].update(location)

def plot_map():
    plt.figure(figsize=(20,10))
    map = Basemap(projection='merc', lon_0=0, resolution='l', llcrnrlon=-180, llcrnrlat=-70, urcrnrlon=180, urcrnrlat=85)
    # draw coastlines, country boundaries, fill continents.
    map.drawcoastlines(linewidth=0.25)
    map.drawcountries(linewidth=0.25)
    map.fillcontinents(color='coral',lake_color='aqua')
    # draw the edge of the map projection region (the projection limb)
    map.drawmapboundary(fill_color='aqua')
    return plt, map

def plot_marker(map):
    max_occurrences = max(ip_occurrence, key=lambda x:ip_occurrence[x]['occurrence'])
    max_occurrences = ip_occurrence[max_occurrences]['occurrence']
    marker_div = max_occurrences / MAX_MARKER_SIZE

    for ip_address in ip_occurrence:
        pos = ip_occurrence[ip_address]['loc'].split(',')
        x, y = map(float(pos[1]), float(pos[0]))
        map.plot(x, y, 'o', markersize = ip_occurrence[ip_address]['occurrence']/marker_div + MIN_MARKER_SIZE, color='gray', alpha=0.8)

def main():

    get_ip_addresses()
    get_locations()

    plt, map = plot_map()
    plot_marker(map)

    plt.show()


if __name__ == "__main__":
    main()
