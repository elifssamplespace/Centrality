import networkx as nx 
import matplotlib.pyplot as plt
from py2neo import Graph, Path ,Node,Relationship,authenticate

authenticate("localhost:7474", "neo4j", "123456")
graph = Graph("http://localhost:7474/db/data/")
tx = graph.cypher.begin()
employee=graph.cypher.execute("Match (e:Deneme) return e.uID")
nodes =graph.cypher.execute("MATCH (t:Deneme)-[r:relation_x]->(e:Deneme) return t.uID,e.uID,r.weigth")
singleton=[1289,1296,1299,1300,1309,1310,1314,1315,1316,1318,1319,1320,1321,1324,1325,1326,1327]

#
# for record in nodes:
#     print record

G=nx.DiGraph();
G.add_nodes_from(singleton)
# G.add_weighted_edges_from(nodes)
for node in nodes:
    G.add_edge(node[0], node[1], weight=node[2])

print nx.info(G)

in_degree_centrality= nx.in_degree_centrality(G,)
out_degree_centrality= nx.out_degree_centrality(G)
closeness_centrality=nx.closeness_centrality(G,distance='weight')
betweenness_centrality=nx.betweenness_centrality(G,weight='weight')
eigenVector_centrality=nx.betweenness_centrality(G,weight='weight')
pr = nx.pagerank(G,weight='weight')

print "In Degree Centrality"
for key, value in sorted(in_degree_centrality.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'

print "Out Degree Centrality"
for key, value in sorted(out_degree_centrality.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'

print "Closeness Centrality"
for key, value in sorted(closeness_centrality.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'

print "Betwenness Centrality"
for key, value in sorted(betweenness_centrality.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'


print "EigenVector Centrality"
for key, value in sorted(eigenVector_centrality.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'




print "Page Rank"
for key, value in sorted(pr.iteritems(), key=lambda (k,v): (v,k)):
    print "Node:%d: %f" % (key, value)
print '\n\n'

nx.draw_networkx(G,pos=nx.spring_layout(G),with_labels='false',node_color='red',edge_color='blue',node_size=75)

plt.axis("off")
plt.show()

