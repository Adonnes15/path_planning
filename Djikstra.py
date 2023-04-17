class pairs:
    def __init__(self,a,b,weight):
        self.vertices=[a,b]
        self.weight=weight



class Nodes:                #creates nodes
    def __init__(self,index,cost=1000):
        self.index=index
        self.cost=cost
        self.neighbours=[]
        self.path=[]
        self.parent=None

    def nodeIndex(self,nodes,p,v):
        for i in nodes:
            if i.index==p.vertices[v]:
                return i
            
    def findNeighbours(self,nodes):     #finds neighbours using common vertices in Links[]
        for p in Links:
            if p.vertices[0]==self.index:
                self.neighbours.append(self.nodeIndex(nodes,p,1))
            elif p.vertices[1]==self.index:
                self.neighbours.append(self.nodeIndex(nodes,p,0))
            else:
                continue


class djikstra:
    def __init__(self):
        temp_indices=[int(i.vertices[0]) for i in Links]       #create nodes
        nodes = []
        self.nodes = []
        for n in temp_indices:
            if n not in nodes and n!=0:
                nodes.append(n)
        self.nodes=[Nodes(a) for a in nodes]
        self.nodes.insert(0,Nodes(0,0))                        # cost of node[0]=0
        for n in self.nodes:
            n.findNeighbours(self.nodes)
        self.update()


    def returnWeight(self,a,b):                                #find weight of a link
        for p in Links:
            if p.vertices==[a,b]:
                return p.weight


    def update(self):
        temp=0
        for a in self.nodes:
            for b in a.neighbours:
                cost=self.returnWeight(a.index,b.index)
                if cost==None:
                    cost=self.returnWeight(b.index,a.index)

                temp=a.cost+cost
                if temp<b.cost:
                    b.cost=temp
                    b.parent=a     
    
    def PathInfo(self):
        for a in self.nodes:
            node=a
            a.path.insert(0,a.index)
            while node.parent!=None:
                a.path.insert(0,node.parent.index)
                node=node.parent

            print("_____________________________")
            print("Node Index:",a.index)
            print("shortest distance:",a.cost)
            print("shortest path:",a.path)


        print("_____________________________")

# pair(vertexA,vertexB,length)
Links=[pairs(0,3,1),pairs(3,5,5),pairs(2,0,5),pairs(2,3,1),pairs(5,2,1),pairs(5,4,2),pairs(4,1,1),pairs(1,2,9)]


if __name__=='__main__':
    test=djikstra()
    test.PathInfo()

