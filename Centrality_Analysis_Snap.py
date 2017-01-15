import snap
from py2neo import Graph, Path ,Node,Relationship,authenticate

#authentication of neo4j for phyton 
authenticate("localhost:7474", "neo4j", "123456")
graph = Graph("http://localhost:7474/db/data/")
tx = graph.cypher.begin()

#linear search method to find singleton nodes
def linear_search(obj, item):
    for i in obj:
        if i== item:
            return 1
    return -1

# returns the nodes with weighted the relations
results = graph.cypher.execute("MATCH (t:Deneme)-[r:relation_x]-(e:Deneme) return t.uID,r.weigth, e.uID")
# return the out degree of nodes
out_degre=graph.cypher.execute("match (n:Deneme)-[r:relation_x]->(e:Deneme) return n.uID,e.uID")
# return the in degree of nodes
in_degre=graph.cypher.execute("match (n:Deneme)<-[r:relation_x]-(e:Deneme) return n.uID,e.uID")
# return all the nodes
employee=graph.cypher.execute("Match (e:Deneme) return e.uID")


# for record in employee:
#     print record
#
# for record in out_degre:
#     print record

# print
#
# for record in in_degre:
#     print record

#finding singleton nodes -----start
singleton= []
node_with_relation = []
for emp in employee:
    for out in out_degre:
        if out[0] == emp[0]:
            node_with_relation+=[ out[0] ] ### Out degre of each node

for emp in employee:
    for input in in_degre:
           if input[0] == emp[0]:
                node_with_relation += [ input[0] ]

for emp in employee:
    if linear_search(node_with_relation,emp[0]) == -1:
        singleton += [ emp[0] ]

# finding singleton nodes ----ends

#print the sigleton nodes --- start
# for s in singleton:
#     print s
#print the sigleton nodes --- ends


# Print graph nodes and edges ---start
def PrintGraph( Graph):
    '''
    Print graph statistics
    '''
    print "nodes %d, edges %d, empty %s" % (
         Graph.GetNodes(), Graph.GetEdges(),
        "yes" if Graph.Empty() else "no")

# Print graph nodes and edges ---ends


#Directed Graph Definition
G= snap.TNGraph.New()

#### Creating nodes and edges
#### Add the nodes to Graph using snap library
for record in out_degre:
    if G.IsNode(record[0]) == False:
        G.AddNode(record[0])
    if G.IsNode(record[1]) == False:
        G.AddNode(record[1])
    G.AddEdge(record[0],record[1])

#### Creating nodes
#### For singleton
for record in singleton:
    G.AddNode(record)

#### Monitoring the Graph
PrintGraph(G)

####Create lists for centrality metrices
OutDegreeCentrality=[];
InDegreeCentrality=[];
ClosenessCentrality=[];
BetweennessCentrality=[];
EigenVectorCentrality=[];
PageRank=[];

##### Degree Centrality ############
## return nodes id and it's in and out degrees
out_degre_centrality=graph.cypher.execute("match (n:Deneme)-[r:relation_x]->() return n.uID, count(*) as OutDegreeScore")
in_degre_centrality=graph.cypher.execute("match (n:Deneme)<-[r:relation_x]-() return n.uID, count(*) as InDegreeScore")

### calculating and sorting degree centrality ----start
for nID in out_degre_centrality:
    OutDegreeCentrality +=[(nID[0],nID[1])]
for nID in in_degre_centrality:
    InDegreeCentrality +=[(nID[0],nID[1])]


InDegreeCentrality.sort(key=lambda  tup: tup[1],reverse=True)
OutDegreeCentrality.sort(key=lambda  tup: tup[1],reverse=True)
### calculating and sorting degree centrality ----end

### print degree centrality
print "Out Degree Centrality"
for record in OutDegreeCentrality:
    print "Node:%d %f" % (record[0], record[1])
print "\n\n"

print "In Degree Centrality"
for record in InDegreeCentrality:
    print "Node:%d %f" % (record[0], record[1])
print "\n\n"

#####Betweenness Centrality ###########
### Create a hashtable for nodes and edges , it's necessary for calculation of betweenness centrality function
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()

### calculating betweenness centrality
snap.GetBetweennessCentr(G, Nodes, 1.0)

### sorting betweenness centrality ----start
for node in Nodes:
    BetweennessCentrality += [(node, Nodes[node])]

BetweennessCentrality.sort(key=lambda  tup: tup[1],reverse=True)
print "Betweennes Centrality"
for record in BetweennessCentrality:
    print "Node:%d %f" % (record[0], record[1])
print
### sorting betweenness centrality ----ends


#####Closeness Centrality###############
## calculating closeness centrality of each node and putting them in a list
for nID in G.Nodes():
    ClosenessCentrality +=[ (nID.GetId(),snap.GetClosenessCentr(G, nID.GetId())) ]

ClosenessCentrality.sort(key=lambda  tup: tup[1],reverse=True)
print "Closeness Centrality"
for record in ClosenessCentrality:
    print "Node:%d %f" % (record[0], record[1])
print





##########Page Rank #############
##### Damping factor is 0.85 (Default)
## create a hashtable  for page rank
PRankH = snap.TIntFltH()
## page rank calculation
snap.GetPageRank(G, PRankH)
## adding them to list
for item in PRankH:
    PageRank += [(item, PRankH[item])]
print

## sorting the list
PageRank.sort(key=lambda  tup: tup[1],reverse=True)
print "PageRank"
for record in PageRank:
    print "Node:%d %f" % (record[0], record[1])
print





######## Eigen Vector Centrality #############
### The graph is converted to undirected graph since eigen vector calculation function does not support directed graph
UnG = snap.ConvertGraph(snap.PUNGraph, G)
### create the hashtable
NIdEigenH = snap.TIntFltH()
### calculation of eigen vector
snap.GetEigenVectorCentr(UnG, NIdEigenH)
### sort the list
for item in NIdEigenH:
    EigenVectorCentrality += [(item, NIdEigenH[item])]
EigenVectorCentrality.sort(key=lambda  tup: tup[1],reverse=True)
print "Eigen Vector Centrality"
for record in EigenVectorCentrality:
    print "Node:%d  %f" % (record[0], record[1])


