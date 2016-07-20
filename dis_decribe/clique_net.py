
from networkx import DiGraph,strongly_connected_components,minimum_node_cut

class clique_net(DiGraph):

	cliques=[]
	topics=[]
	topic_cliq=[]

	def load_cliques(self,cliques):

		self.cliques=cliques

		for k in range(len(cliques)):
			DiGraph.add_node(self,k,keywords=cliques[k])
		for i in range(len(cliques)):
			for j in range(i):
				a=set(cliques[i])
				b=set(cliques[j])
				common_words=len(a.intersection(b))
				dis_i2j=common_words/len(a)
				dis_j2i=common_words/len(b)
				if dis_i2j>0:
					DiGraph.add_edge(self,i,j,weight=dis_i2j)
				if dis_j2i>0:
					DiGraph.add_edge(self,j,i,weight=dis_j2i)

	'''def mean_in_degree(self):
		nodes=DiGraph.nodes(self)
		sum=0.0
		for node in nodes:
			 sum=sum+DiGraph.in_degree(self,node)
		mean_in_degree=sum/float(len(nodes))
		return mean_in_degree

	def median_in_degree(self):
		nodes=DiGraph.nodes(self)
		mlist=[]
		for node in nodes:
			 mlist.append(DiGraph.in_degree(self,node))
		n=len(mlist)
		mlist=sorted(mlist)
		if n%2==0:
			x=mlist[round(n/2)]+mlist[round(n/2)+1]
			median_in_degree=round(x/2)
		else:
			median_in_degree=mlist[round(n/2)]
		return median_in_degree'''
		
	def mean_weight(self):
		edges=DiGraph.edges(self,data='weight')
		sum=0.0
		for edge in edges:
			sum=sum+edge[2]
		mean_weight=sum/float(len(edges))
		return mean_weight
		
	def median_weight(self):
		edges=DiGraph.edges(self,data='weight')
		mlist=[]
		for edge in edges:
			mlist.append(edge[2])
		n=len(mlist)
		mlist=sorted(mlist)
		if n%2==0:
			x=mlist[round(n/2)]+mlist[round(n/2)+1]
			median_weight=float(x)/float(2)
		else:
			median_weight=mlist[round(n/2)]
		return median_weight
		
	def filter_nodes(self,thresh):
		nodes=DiGraph.nodes(self)
		for node in nodes:
			if DiGraph.in_degree(self,node)<thresh:
				DiGraph.remove_node(self,node)

		nodes=DiGraph.nodes(self)
		for node in nodes:
			if DiGraph.in_degree(self,node)==0 and DiGraph.out_degree(self,node)==0:
				DiGraph.remove_node(self,node)

	def filter_edges(self,thresh):
		edges=DiGraph.edges(self,data='weight')
		for edge in edges:
			if edge[2]<thresh:
				DiGraph.remove_edge(self,edge[0],edge[1])

				if DiGraph.in_degree(self,edge[0])==0 and DiGraph.out_degree(self,edge[0])==0:
					DiGraph.remove_node(self,edge[0])

				if DiGraph.in_degree(self,edge[1])==0 and DiGraph.out_degree(self,edge[1])==0:
					DiGraph.remove_node(self,edge[1])

	def splitG(self,minN):
		contcmp=[]
		ct_cliq=[]

		cncp=list(strongly_connected_components(self))
		for item in cncp:
			#print(len(item))
			if len(item)<=minN and len(item)>1:
				#print("topic")
				tmp=set()
				tmp_cliq=[]
				for each in item:
					tmp=tmp.union(set(self.node[each]["keywords"]))
					tmp_cliq.append(each)
					DiGraph.remove_node(self,each)
				contcmp.append(tmp)
				ct_cliq.append(tmp_cliq)
			if len(item)==1:
				DiGraph.remove_node(self,list(item)[0])

		nodes=DiGraph.nodes(self)
		for node in nodes:
			if DiGraph.in_degree(self,node)==0 and DiGraph.out_degree(self,node)==0:
				DiGraph.remove_node(self,node)

		return contcmp,ct_cliq



	def merge(self,minN):
		
		import numpy as np
		merged=[]
		merged_cliq=[]
		while len(DiGraph.nodes(self)):
			#print(len(self.nodes()))
			contcmp,ct_cliq=self.splitG(minN)

			if not DiGraph.nodes(self):
				break
			merged=merged+contcmp 
			merged_cliq=merged_cliq+ct_cliq

			try:
				#print("point1")
				cut_nodes=minimum_node_cut(self)

				#print("point2")
			except:
				nodes=DiGraph.nodes(self)
				index=np.random.randint(len(nodes))
				cut_nodes=[nodes[index]]

			for node in cut_nodes:
				DiGraph.remove_node(self,node)

		self.topics=merged
		self.topic_cliq=merged_cliq

