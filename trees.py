import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from shapely.geometry import Polygon,LineString,Point
import random

class treeNode:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.parent=None
        self.children=[]

    def SetParent(self,parent):
        self.parent=parent
        parent.children.append(self)

class RRTAlgorithm:
    def __init__(self,start,goal,obstacle_list,mapdimensions,stepsize,maxIter):
        self.start=treeNode(start[0],start[1])
        self.goal=treeNode(goal[0],goal[1])
        self.Links=[self.start]
        self.nLinks=0
        self.new_node=self.start
        self.maxIter=maxIter
        self.r=stepsize
        self.finalPath=[self.goal]
        self.intersect=True
        self.TargetRegion=5
        self.obstacle_list=obstacle_list
        self.mapw,self.maph=mapdimensions
        self.plotStatic()
        self.Explore()

    def AddChild(self,node,parent):
        tempNode=node
        tempNode.SetParent(parent)
        self.Links.append(self.new_node)
        self.nLinks+=1

    def NearestNode(self,sample):
        temp=0
        for i in range(len(self.Links)):
            if self.distance(sample,self.Links[i])<self.distance(sample,self.Links[temp]):
                temp=i
        return self.Links[temp]

        # distances = [self.distance(sample, node) for node in self.Links]
        # min_idx = np.argmin(distances)
        # return self.Links[min_idx]
    

    def distance(self,point,node1):
        distance=np.sqrt((point.x-node1.x)**2+(point.y-node1.y)**2)
        return distance

    def SampleAPoint(self):
        X=int(random.uniform(1, self.mapw - 1))
        Y=int(random.uniform(1, self.maph - 1))
        return treeNode(X,Y)

    def steerToPoint(self,sample,node0):
        dist = self.distance(sample,node0)
        if dist < self.r:
            return sample
        else:
            theta=np.arctan2(sample.y-node0.y,sample.x-node0.x)
            self.intersect=self.intersecting(node0.x,node0.y,theta)
            Xnode=node0.x+self.r*np.cos(theta)
            Ynode=node0.y+self.r*np.sin(theta)
            return treeNode(Xnode,Ynode)

    def InObstacle(self,x,y):
        n = len(self.obstacle_list)

        p = Point(np.array([x,y]))
        for i in range(n):
            poly = Polygon(self.obstacle_list[i])
            if p.within(poly):
                return False
        return True

    def intersecting(self,x,y,theta):
        r=self.r/500
        for i in range(0,500):
            x+= r*np.cos(theta)
            y+= r*np.sin(theta)
            if not self.InObstacle(x,y):
                return False
        return True
            


    def retraceRRTPath(self):
        backNode=self.new_node
        while backNode!=self.start:
            self.finalPath.insert(0,backNode)
            backNode=backNode.parent
        self.finalPath.insert(0,self.start)
         

        for i in range(len(self.finalPath)-1):
            plt.plot([self.finalPath[i].x,self.finalPath[i+1].x],[self.finalPath[i].y,self.finalPath[i+1].y],'ro-')
            plt.pause(0.05)



    def Explore(self):
        for i in range(self.maxIter):
           
            if self.distance(self.new_node,self.goal)>=self.TargetRegion:
                randomPoint=self.SampleAPoint()
                self.closestNode=self.NearestNode(randomPoint)
                self.new_node=self.steerToPoint(randomPoint,self.closestNode)
                if self.InObstacle(self.new_node.x,self.new_node.y) and self.intersect:
                    self.AddChild(self.new_node,self.closestNode)
                    plt.plot([self.new_node.x,self.closestNode.x],[self.new_node.y,self.closestNode.y],color='#1589FF',linewidth='1.5',marker='o',linestyle='-',markersize='5',markeredgecolor='#0000CD')
                plt.axis('equal')
                plt.title("RRT")
                # self.closestNode=None
                # randomPoint=None
            else:
                self.retraceRRTPath()
                plt.pause(1)
                break
            plt.pause(0.05)
        plt.show()

    def plotStatic(self):
        fig, axs = plt.subplots()
        plt.xlim([0, self.mapw])
        plt.ylim([0, self.maph])
        plt.plot(self.start.x,self.start.y,'ro')
        plt.plot(self.goal.x,self.goal.y,'go')
        region = Circle((self.goal.x, self.goal.y), self.TargetRegion, color = '#1DA306',fill=False)

        plt.gca().add_patch(region)
        fig.tight_layout()

        axs.set_aspect('equal', 'datalim')
    
        n = len(self.obstacle_list)
        for i in range(n):
            poly = Polygon(self.obstacle_list[i])   
            axs.fill(*poly.exterior.xy, fc='black', ec='none')
            # plt.plot(*poly.exterior.xy,c='black')



if __name__=='__main__':
    start=np.array([1,1])
    goal=np.array([80,80])
    # listofobstacles = [[(25,25),(25,50),(75,50),(75,25)],[(10, 10), (20, 20), (10, 30), (0, 20)],[(70,10),(60,10),(65,20)]]   
    listofobstacles = [[(40, 0), (40, 40), (50, 50), (60, 40), (50, 40)],[(10, 10), (20, 20), (10, 30), (0, 20)],[(50, 60), (70, 80), (60, 100), (40, 80), (45, 100)],[(70, 20), (90, 20), (80, 40)]]
    
    RRTAlgorithm(start,goal,listofobstacles,(100,100),5,10000)