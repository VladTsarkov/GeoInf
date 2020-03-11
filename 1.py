from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass

from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()

from math import cos,sin,radians,fabs
R = 6371
def get_cartesian(x,y):#x - lat, y - lon(dolgota)
    x,y = R * cos(radians(x))*cos(radians(y)), R * cos(radians(x))*sin(radians(y))
    return x,y
#pазобраться с широтой и долготой, как передает их osm
def get_cart(temp):
    #print('1st ',temp)
    if temp["type"]=="Polygon":
        temp = temp["coordinates"][0]
        for i in temp:
            i[0],i[1] = get_cartesian(i[0],i[1])
    elif temp["type"]=="LineString":
        temp = temp["coordinates"]
        for i in temp:
            i[0],i[1] = get_cartesian(i[0],i[1])
    else:
        print("Another TYPE ! ", temp["type"])
    #print('2nd ',temp)
    return temp
def get_Gaus_area(temp):
    sum,raz = 0,0
    n = len(temp)
    for i in range(n-1):
        sum += temp[i][0]*temp[i+1][1] - temp[i+1][0]*temp[i][1]
        #if i != 0:
        #    raz += temp[i][0] * temp[i-1]
    sum += temp[n-1][0]*temp[0][1] - temp[0][0]*temp[n-1][1]
    return fabs(sum/2)
"""
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
nyc = nominatim.query('Perm')
print(nyc.toJSON())"""

#query = overpassQueryBuilder(bbox=[58.0065792, 56.2248863, 58.0103644, 56.2305674], elementType=['way','node'], selector='building', out='body',includeGeometry=True)

#query = overpassQueryBuilder(area=nominatim.query('Perm').areaId(), elementType=['way','node'], selector=['building','"name"="Ленинский район"'], out='body',includeGeometry=True)
#query = overpassQueryBuilder(area=nominatim.query('Perm, Свердловский район').areaId(), elementType=['way','node'], selector=['building'], out='body',includeGeometry=True)
query = overpassQueryBuilder(area=nominatim.query('Perm, Свердловский район').areaId(), elementType=['way','node'], selector=['building'], out='body',includeGeometry=True)

overpass = Overpass()

huh = overpass.query(query)
#print(huh.ways())
print(huh.countElements())
print(huh.countWays())
living_houses_w_levels = ['yes','apartments','dormitory','residential']
living_houses_wo_levels = ['house','bungalow','detached']
unliving_houses = ['roof', 'university', 'kindergarten', 'school', 'retail', 'commercial', 'office', 'church',
 'hotel', 'garages', 'construction', 'train_station', 'cathedral', 'supermarket', 'service', 'offices',
 'mosque', 'hospital', 'college', 'garage', 'warehouse', 'industrial', 'kiosk']
check_build=[]
people = 0
max = 0
for n in huh.ways():
    #print(n.tag("building"))
    #print(n.tags())
    #print(n.id())
    #print(n.geometry())
    #temp = get_cart(n.geometry()["coordinates"][0])
    temp = get_cart(n.geometry())
    area = get_Gaus_area(temp)*1000000
    #print(n.tags(), area)
    #if n.tag("building") not in check_build:
    #    check_build.append(n.tag("building"))
    if n.tag("amenity") == None and n.tag("shop") == None and n.tag("tourism") == None:
        if n.tag("building") in living_houses_w_levels:
        #if n.tag("building") in living_houses_w_levels:
            if "building:levels" in n.tags():
                if int(n.tag("building:levels"))>2:
                    #print("Huh")
                    people += area/22/2*(int(n.tag("building:levels"))-2)
                    #print(n.tags(), area, area/22/2*(int(n.tag("building:levels"))-2))
                    """
                    if area/22*(int(n.tag("building:levels"))-2) > 1500:
                        print(n.tags(), area, area/22*(int(n.tag("building:levels"))-2))

                    if max < area/22*(int(n.tag("building:levels"))-2):
                        max = area/22*(int(n.tag("building:levels"))-2)
                        print(n.tags(), area, area/22*(int(n.tag("building:levels"))-2))
                    """
                else:
                    people += area/22
                    #if max < area/22:
                    #    max = area
                    #print(n.tags(), area, area/22)
            else:
                people += area/22
                #if max < area/22:
                #    max = area
                #print(n.tags(), area, area/22)
        elif n.tag("building") in living_houses_wo_levels:
        #elif n.tag("building") in living_houses_wo_levels:
            people += area/22
            #if max < area/22:
            #    max = area
            #people += 3
            #print(n.tags(), area, area/22)
        else:
            if n.tag("building") not in check_build:
                check_build.append(n.tag("building"))
                #print(n.tags())
#print(huh.ways()[0].geometry()["coordinates"][0])
#query = overpassQueryBuilder(bbox=[48.1, 16.3, 48.3, 16.5], elementType='node', selector='"highway"="bus_stop"', to='2020-02-02T00:00:00Z',out='body')
#busStops = overpass.query(query)
print("Number of people = ",people)
print("houses = ",check_build)
