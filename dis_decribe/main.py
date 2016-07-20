from decribeprocess import decribeprocess
from clique_net import clique_net               
#from cusum  import process,plot,cusum                              

dis="高血压"
				
if __name__=="__main__":

	decribe=decribeprocess(dis)
	#可以从数据库中或从文件中读取疾病描述文本

	#从文件读取
	decribe.readwb("%s.txt" %dis)

	#从数据库读取
	#decribe.search_decribe(dis)

	decribe.concurrence()#词共现
	print("keywords network mean edge:%.2f"%(decribe.mean_edge()))
	print("keywords network median edge:%.2f"%(decribe.median_edge()))
	print("remove_edge with median edge+3:%.2f"%(decribe.median_edge()+3))
	decribe.remove_edge(decribe.median_edge()+3)#中值+3，过滤边
	G=decribe.multi_graph_construct()#词共现网络
	cliques=decribe.find_cliques(G)#max clique
	#print("the found cliques")
	#print(cliques)
	print("found %d cliques!"%(len(cliques)))
	
	G=clique_net()
	import pickle
	import networkx as nx
	
	print("build cliques net")
	G.load_cliques(cliques)
	#print(len(G.cliques))
	
	#过滤结点参数设置，设置成总clique个数的1/10，也可以根据结果调节
	thresh=len(G.cliques)/10
	print("filter nodes with the number of clique/10: %f"%(thresh))
	G.filter_nodes(thresh)

	#过滤边，设置成0.5，可调节
	print("clique_net edges mean_weight :%f"%(G.mean_weight()))
	print("clique_net edges median_weight :%f"%(G.median_weight()))
	print("filter edges with median_weight*2:%f"%(G.median_weight()*2))
	G.filter_edges(G.median_weight()*1.5)

	print(len(G.nodes()))

	print("merging")
	G.merge(30)
	f = open("%s"%(dis), 'w')  
	for item in G.topics:
		print(item)
		print(item, file=f)  
	print("merged")
	f.close()
	# topics_time=G.topic_decribe(decribe,dis)
	# #G.plot_topic(topics_time)
	
	# topics,topic_time=process("topic_decribe_%s.txt" %dis)
	# cusum(topics,topic_time,10,dis)
