from OSMPythonTools.overpass import overpassQueryBuilder
from OSMPythonTools.overpass import Overpass

from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()

from math import cos,sin,radians,fabs, inf
from progn import Character
R = 6371
def get_cartesian(x,y):#x - lat, y - lon(dolgota)
    x,y = R * cos(radians(x))*cos(radians(y)), R * cos(radians(x))*sin(radians(y))
    return x,y
#pазобраться с широтой и долготой, как передает их osm
def get_cart(temp):
    # print('1st ',temp)
    minx,miny,maxx,maxy = inf, inf, 0, 0
    for shop in temp:
        # print(temp[shop])
        # print(shop["coordinates"])
        for coord in temp[shop]["coordinates"]:
            coord[0],coord[1] = get_cartesian(coord[0],coord[1])
            if minx > coord[0]:
                minx = coord[0]
            if miny > coord[1]:
                miny = coord[1]
            if maxx < coord[0]:
                maxx = coord[0]
            if maxy < coord[1]:
                maxy = coord[1]
    return minx,miny,maxx,maxy
def get_Gaus_area(temp):
    sum,raz = 0,0
    n = len(temp)
    for i in range(n-1):
        sum += temp[i][0]*temp[i+1][1] - temp[i+1][0]*temp[i][1]
        #if i != 0:
        #    raz += temp[i][0] * temp[i-1]
    sum += temp[n-1][0]*temp[0][1] - temp[0][0]*temp[n-1][1]
    return fabs(sum/2)
class Wall:
    def __init__(self,w,h):
        self.w = w
        self.h = h
        self.wall = [[1 if i==0 or j==0 or i ==w or j==h else 0 for j in range(h+1)]for i in range(w+1)]

    def draw_box(self):
        for i in range(self.w+1):
            for j in range(self.h+1):
                print(self.wall[i][j],end = '')
            print()
        return None

    def find_max_density(self,k):
        for i in range(self.w+1):
            for j in range(self.h+1):
                if self.wall[i][j] == k:
                    return i,j
        return None
"""
from OSMPythonTools.nominatim import Nominatim
nominatim = Nominatim()
nyc = nominatim.query('Perm')
print(nyc.toJSON())"""

#query = overpassQueryBuilder(bbox=[58.0065792, 56.2248863, 58.0103644, 56.2305674], elementType=['way','node'], selector='building', out='body',includeGeometry=True)

#query = overpassQueryBuilder(area=nominatim.query('Perm').areaId(), elementType=['way','node'], selector=['building','"name"="Ленинский район"'], out='body',includeGeometry=True)
#query = overpassQueryBuilder(area=nominatim.query('Perm, Свердловский район').areaId(), elementType=['way','node'], selector=['building'], out='body',includeGeometry=True)
#query = overpassQueryBuilder(area=nominatim.query('Perm, Ленинский район').areaId(), elementType=['way','node'], selector=['shop'], out='body',includeGeometry=True)
area = nominatim.query('Perm, Ленинский район')
#area = nominatim.query('Perm, Ленинский район',wkt=True)
query = overpassQueryBuilder(area.areaId(), elementType=['way','node'], selector=['shop'], out='body',includeGeometry=True)

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
check_shops = []
shops = {}
id = 0
for n in huh.ways():
    #print(n.tags())
    #print(n.id())
    #print(n.geometry())
    sr = 0
    x, y = 0, 0
    for i in n.geometry()["coordinates"][0]:
        #x, y, sr += i[0], i[1], 1
        x += i[0]
        y += i[1]
        sr += 1
    #print(n.geometry()["coordinates"][0], "srednee ", sr, " otvet ",x/sr,y/sr)

    if n.tag("shop") not in shops:
        shops.update({n.tag("shop"):{"count":1,"id":id,"coordinates":[[x/sr,y/sr]]}})
        id+=1
    else:
        shops[n.tag("shop")]["count"]+=1
        shops[n.tag("shop")]["coordinates"].append([x/sr,y/sr])
    if n.tag("shop") not in check_shops:
        check_shops.append(n.tag("shop"))
        #print(n.tags())
for n in huh.nodes():
    #print(n.tags())
    #print(n.id())
    #print(n.geometry())
    if n.tag("shop") not in shops:
        shops.update({n.tag("shop"):{"count":1,"id":id,"coordinates":[n.geometry()["coordinates"]]}})
        id+=1
    else:
        shops[n.tag("shop")]["count"]+=1
        shops[n.tag("shop")]["coordinates"].append(n.geometry()["coordinates"])
        #print(shops[n.tag("shop")]["coordinates"])
    if n.tag("shop") not in check_shops:
        check_shops.append(n.tag("shop"))
        #print(n.tags())
shops2 = shops.copy()
print(shops)
minx,miny,maxx,maxy = get_cart(shops2)
#print(shops2)
print(minx,miny,maxx,maxy)
print(0,0,(maxx-minx)*1000,(maxy-miny)*1000)
print(0,0,round((maxx-minx)*10)*10,round((maxy-miny)*10)*10)
print(area.toJSON())


temp = []
for i in shops2["kiosk"]["coordinates"]:
    temp.append([round((i[0]-minx)*10)*10,round((i[1]-miny)*10)*10])
print("TEMP ",temp)
a = Wall(round((maxx-minx)*10)*10,round((maxy-miny)*10)*10)
d = [i for i in range(len(temp))]
b = [i for i in range(len(temp))]
k = [i for i in range(len(temp))]
for i in range(len(temp)):
    d[i] = Character(temp[i][0],temp[i][1],a.wall)
    b[i] = 0
    k[i] = 0
    #print(temp[i])
while True:
    for i in range(len(temp)):
        b[i], k[i] = d[i].step(a.wall)
    #for i in range(len(temp)):
    #    print(b[i], end=' ')
    if b.count(0) == len(temp):
        break
maxt = 0
for i in range(len(temp)):
    if maxt < k[i]:
        maxt = k[i]
print("\nMAX density =",maxt)
print(a.find_max_density(maxt))
#print(a.find_max_density(22))

"""
a = Wall(9,9)
a1 = Character(5,2,a.wall)
steps = []
a2 = Character(7,4,a.wall)
a3 = Character(2,7,a.wall)

while True:
    b1,k1 = a1.step(a.wall)
    b2,k2 = a2.step(a.wall)
    b3,k3 = a3.step(a.wall)
    if b1 == 0 and b2 == 0 and b3 == 0:
        break

a.draw_box()
print("\nMAX density =",max(k1,k2,k3))
print(a.find_max_density(max(k1,k2,k3)))
"""

#print(area.wkt())
for i in shops:
    print(i, "[" ,shops[i]["id"], "] kolvo ", shops[i]["count"])
