#!/usr/bin/env python3
#Following is the import line for importing the obstacle detection methods i.e. isValidPoint()
#you need to name this node as "path_planner"
import rospy
import obstacle_detection as obsdet
from robotics_hackathon_automation.msg import NextPoint
from robotics_hackathon_automation.msg import PointList

import random
from turtle import distance
from xmlrpc.server import DocXMLRPCRequestHandler
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from shapely.geometry import LineString
import obstacle_detection as obsDet
from math import atan2

class planner:
    def __init__(self, path, obstacles):

        rospy.init_node("path_planner")

        pub = rospy.Publisher("/planned_path", PointList, queue_size = 10)

        r = rospy.Rate(1)
        self.path = path
        self.list = []
        xp,yp = path[0]
        new_path = []
        new_path.append((xp,yp))
        for i in range(1,len(self.path)):
            xc,yc = self.path[i]
            if i<len(self.path)-1:
                if atan2(self.path[i][1] - yp, self.path[i][0] - xp) != atan2(self.path[i+1][1] - yp, self.path[i+1][0] - xp):
                    xp,yp = self.path[i]
                    new_path.append((xp,yp))	
                elif (xc,yc) in [(-4, -2), (-3, 2), (-1, -2), (0.3, 0.2), (1.36, -1.8)]:
                    xp,yp = xc,yc
                    new_path.append((xp,yp))
            else:
                new_path.append(self.path[i])
        counter = 0
    

        l = len(new_path)
        
        for i in range(l):
            x, y = new_path[i]
            point = NextPoint()
            point.x = x
            point.y = y
            self.list.append(point)

        while not rospy.is_shutdown():
            if counter <= 1:
                pub.publish(self.list)
                counter = counter + 1
            r.sleep()

class dijkstra: #operating as A*

    def __init__(self, n, listOfNodes, paths):

        self.n = n
        self.pathLen = []
        self.viaNode = []
        self.done = []
        self.all = []
        self.listOfNodes = listOfNodes
        self.paths = paths
        self.onePath = []
        self.finalPath = []

        self.declarepathLen()
        self.declareviaNode()
        self.declareall()

    def declarepathLen(self):
        # self.pathLen.append(0)
        for i in range(self.n):
            self.pathLen.append(1000)

    def declareviaNode(self):
        for i in range(self.n):
            self.viaNode.append(0)

    def declareall(self):
        for i in range(self.n):
            self.all.append(i)

    def dist(self, a, b):
        x1, y1 = self.listOfNodes[a]
        x2, y2 = self.listOfNodes[b]
        dist = ((x2 - x1)**2+(y2-y1)**2)**0.5
        return dist

    def addToDoneList(self, a):
        self.done.append(a)

    def nextNode(self): #Use for dijkstra
        pathLen = self.pathLen.copy()
        done = self.done.copy()
        all = self.all.copy()
        left = list(set(all) - set(done))
        a = left.pop(0)
        min = pathLen[a]
        while left != []:
            b = left.pop(0)
            if pathLen[b] < min:
                a = b
        return a

    def nextNodeHuer(self, c): #Use for Astar
        pathLen = self.pathLen.copy()
        done = self.done.copy()
        all = self.all.copy()
        left = list(set(all) - set(done))
        a = left.pop(0)
        min = pathLen[a] + self.dist(a, c)
        while left != []:
            b = left.pop(0)
            if pathLen[b] + self.dist(b, c) < min:
                a = b
                min = pathLen[a] + self.dist(a,c)
        return a
        
    def drawLine(self, a, b):
        x1, y1 = self.listOfNodes[a]
        x2, y2 = self.listOfNodes[b]
        plt.plot([x1, x2], [y1, y2], color = 'black')

    def clear(self):
        self.pathLen = []
        self.viaNode = []
        self.done = []
        self.onePath = []

        self.declarepathLen()
        self.declareviaNode()

class obstacles:

    def drawObs(self):
        Wall = obsDet.Wall
        display_maze = [Wall(-5.191, 0.9886, 1, 0.15), Wall(-5.639, -0.8309, 0.15, 3.769200), Wall(-5.672, 1.785, 0.15, 1.597130), Wall(-4.957, 2.543, 1.597130, 0.15), Wall(-4.277, 2.007956, 0.15, 1.169920), Wall(-0.0037, 2.51, 8.729630, 0.15), Wall(-1.588, 1.8136, 0.15, 1.25), Wall(-1.588, 0.0886, 0.15, 2.5), Wall(-2.138, 1.26, 1.25, 0.15), Wall(-2.668, 0.7136, 0.15, 1.25), Wall(-3.488, 0.16, 1.75, 0.15), Wall(2.405, 0.656, 0.75, 0.15), Wall(2.705, 0.956, 0.15, 0.75), Wall(3.2522, 1.2566, 1.25, 0.15), Wall(3.80526, 0.2066, 0.15, 2.25), Wall(3.3802, -0.844, 1, 0.15), Wall(2.955, -0.5433, 0.15, 0.75), Wall(2.7802, -0.2433, 0.5, 0.15), Wall(2.605, -0.5433, 0.15, 0.75), Wall(4.301, 2.189, 0.15, 0.810003), Wall(4.975, 2.5196, 1.50, 0.15), Wall(5.711, 1.998, 0.15, 1.192330), Wall(5.306, 1.463, 0.919672, 0.15), Wall(5.698, 0.301, 0.15, 2.276490), Wall(5.185, -0.885, 1.119670, 0.15), Wall(4.7, -1.296, 0.15, 0.982963), Wall(5.67, -1.7033, 0.15, 1.75), Wall(5.154, -2.521, 1.185380, 0.15), Wall(0.673, -2.534, 7.883080, 0.15), Wall(1.906, -1.93, 0.15, 1.206910), Wall(0.877, -1.7, 0.15, 1.719980), Wall(0.2502, -0.917, 1.50, 0.15), Wall(-0.433, -1.389, 0.15, 1.072), Wall(-0.4292, -0.4799, 0.15, 0.927565), Wall(0.9177, 0.2156, 0.15, 2.416050), Wall(0.23527, 1.3486, 1.5, 0.15), Wall(-0.439, 1.048, 0.15, 0.75), Wall(-3.2627, -1.72, 0.15, 1.75), Wall(-3.883, -0.9203, 1.414750, 0.15), Wall(-3.9377, -2.52, 1.5, 0.15), Wall(-4.615, -2.157, 0.15, 0.870384), Wall(2.105, 1.58, 0.15, 2.15893)]
        for wall in display_maze:
            x, y = wall.polygon.exterior.xy
            plt.plot(x, y)

    def doesNotBelong(self, x, y):
        return not obsDet.isPointInObstacles(x, y)

    def doesNotIntersect(self, x, y, xn, yn):
        i=1
        while i<101:
            xco = (x*(100-i)+xn*i)/100
            yco = (y*(100-i)+yn*i)/100
            if not self.doesNotBelong(xco,yco):
                return False
            i=i+1
        return True

class grid:

    def __init__(self):
        self.gridLength = 25
        self.gridHeight = 15
        self.length = 11.4
        self.height = 5.4
        self.startx = -5.7
        self.starty = -2.7
        self.listOfNodes = []
        self.listOfRoads = []
        self.dx = self.length/(self.gridLength-1)
        self.dy = self.height/(self.gridHeight-1)
        self.dist = ((self.dx)**2+(self.dy)**2)**0.5 + 0.05
        
        plt.xlim([-6, 6])
        plt.ylim([-3, 3])


        self.generateList()
        self.drawRoads()

        
    def generateList(self):
        x = self.gridLength-1
        y = self.gridHeight-1
        for i in range(x):
            for j in range(y):
                xn, yn = self.Coords(i, j)
                if not obsDet.isPointInObstacles(xn, yn):
                    self.listOfNodes.append((xn, yn))
                    self.drawNode(xn, yn, 0)

    
    def Coords(self, x, y):
        xn = self.startx + x*(self.dx)
        yn = self.starty + y*(self.dy)
        return xn, yn

    def drawNode(self, x, y, flag):
        if flag==0:
            node = Circle((x, y), 0.05, color = 'r')
        else:
            node = Circle((x, y), 0.05, color = 'g')
        plt.gca().add_patch(node)

    def drawRoads(self):
        listOfNodes = self.listOfNodes.copy()
        n = len(listOfNodes)
        num = 0
        for i in range(n):
            x, y = listOfNodes[i]
            num = num + 1
            percent = (num/n)*100
            print(f"Path Progress: {percent}%")
            f = 0
            for j in range (n):
                if f == 8:
                    break
                xn, yn = listOfNodes[j]
                if self.distance(x, y, xn,yn)<=self.dist and obstacles.doesNotIntersect(xn, yn, x, y) and not(xn == x and yn == y):
                    if not self.alreadyInserted(xn, yn, x, y):
                        self.drawLine(xn, yn, x, y)
                        self.addToList(xn, yn, x, y)
                    f = f + 1

    def alreadyInserted(self, x, y, xn, yn):
        listofroads = self.listOfRoads 
        l = len(self.listOfRoads)
        for i in range(l):
            if x == listofroads[i][0] and y == listofroads[i][1] and xn == listofroads[i][2] and yn == listofroads[i][3]:
                return True
            if xn == listofroads[i][0] and yn == listofroads[i][1] and x == listofroads[i][2] and y == listofroads[i][3]:
                return True
        return False

    def distList(self, x, y):
        listOfNodes = self.listOfNodes.copy()
        listOfDist = []
        while listOfNodes != []:
            xn, yn = listOfNodes.pop(0)
            listOfDist.append(self.distance(xn, yn, x, y))
        listOfDist.sort()
        listOfDist.pop(0) #Remove the point itself
        return listOfDist

    def distance(self, x1, y1, x2, y2):
        dist = ((x2 - x1)**2+(y2-y1)**2)**0.5
        return dist

    def atDist(self, d, x, y):
        listOfNodes = self.listOfNodes.copy()
        while listOfNodes != []:
            xn, yn = listOfNodes.pop(0)
            if self.distance(xn, yn, x, y)==d:
                return xn, yn   

    def drawLine(self, xn, yn, x, y):
        plt.plot([x, xn], [y, yn], color='#99E6FF')

    def addToList(self, xn, yn, x, y):
        self.listOfRoads.append((xn, yn, x, y))

    def addList(self, list):
        l = len(list)
        for i in range (l):
            x, y = list[i]
            self.listOfNodes.append((x,y))

        k = len(self.listOfNodes)
        for i in range (l):
            x, y = self.listOfNodes[k-l+i]
            for j in range (k):
                xn, yn = self.listOfNodes[j]
                if self.distance(x, y, xn,yn)<=0.5 and obstacles.doesNotIntersect(xn, yn, x, y) and not(x == xn and y == yn):
                    if not self.alreadyInserted(xn, yn, x, y):
                        self.drawLine(xn, yn, x, y)
                        self.addToList(xn, yn, x, y)

    def make_list_of_paths(self):
        list_of_paths = []
        list_of_nodes = self.listOfNodes.copy()
        l = len(list_of_nodes)
        for i in range(l):
            x,y = list_of_nodes.pop(0)
            list_of_connected_nodes = self.list_of_connected_nodes(x,y)
            list_of_paths.append(list_of_connected_nodes)
        return list_of_paths

    def list_of_connected_nodes(self,x,y):
        listofroads = self.listOfRoads.copy()
        list_of_index = []
        l = len(listofroads)
        for i in range(l):
            if x == listofroads[i][0] and y==listofroads[i][1]:
                xn,yn = listofroads[i][2] , listofroads[i][3]
                index = self.find_index(xn,yn)
                if self.not_in_index_list(index,list_of_index):
                    list_of_index.append(index)
            if x == listofroads[i][2] and y==listofroads[i][3]:
                xn,yn = listofroads[i][0] , listofroads[i][1]
                index = self.find_index(xn,yn)
                if self.not_in_index_list(index,list_of_index):
                    list_of_index.append(index)
            
        return list_of_index

    def not_in_index_list(self,index,list_of_index):
        l = len(list_of_index)
        for i in range(l):
            if index == list_of_index[i]:
                return False
        return True

    def find_index(self,x,y):
        l = len(self.listOfNodes)
        for i in range(l):
            if x==self.listOfNodes[i][0] and y==self.listOfNodes[i][1]:
                return i
   


#PRM
obstacles = obstacles()
obstacles.drawObs()

myGrid = grid()

listOfStops = [(-5.06, -3.12), (-4, -2), (-3, 2), (-1, -2), (0.3, 0.2), (1.36, -1.8)]


#A*
myGrid.addList(listOfStops)
listOfNodes = myGrid.listOfNodes.copy()

paths = myGrid.make_list_of_paths()

k = len(listOfNodes)
dstra = dijkstra(k, listOfNodes, paths)

l = len(listOfStops)

print("finding path")
for i in range(l-1):

    startNode = k-l+i
    endNode = k-l+i+1
    
    dstra.pathLen[startNode] = 0

    
    a = startNode
    while a != endNode :
        b = dstra.paths[a]
        b = list(set(b) - set(dstra.done))
        while b != []:
            c = b.pop(0)
            dist = dstra.dist(a, c) + dstra.pathLen[a] 
            if dist < dstra.pathLen[c]:
                dstra.pathLen[c] = dist
                dstra.viaNode[c] = a
        dstra.addToDoneList(a)
        a = dstra.nextNodeHuer(endNode)
    
    a = endNode
    dstra.onePath.append(dstra.listOfNodes[a])

    
    while True:
        b = dstra.viaNode[a]
        dstra.onePath.append(dstra.listOfNodes[a])
        dstra.drawLine(a, b)
        a = b
        if b == startNode:
            break
    dstra.onePath.reverse()
    dstra.finalPath = dstra.finalPath + dstra.onePath
    dstra.clear()


plt.show()
# Loop through all points and check if current and start node are valid connects
# Check if current is goal

# dstra.finalPath
planner = planner(dstra.finalPath, obstacles)
