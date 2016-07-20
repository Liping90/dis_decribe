import jieba.analyse
import os
import pickle

class decribeprocess():
	keywords=[]
	concurrence={}
	decribe=[]

	def __init__(self,dis):
                self.dis=dis
        
	def readwb(self,filepath):

		newfile=filepath.strip("\n").strip().split('.')[0]+".pkl"
		if os.path.isfile(newfile):
			info=pickle.load(open(newfile,"rb"))
			self.keywords=info["text"]
			self.decribe=info["decribe"]


		else:
			keywords=[]
			stopwords=[]
			decribe=[]
			mydict=[]
			with open("lib/mydict.txt",encoding="utf-8") as disdict:
				for line in disdict:
					line=line.strip('\n').strip()
					mydict.append(line)
					
			if self.dis not in mydict:
				with open("lib/mydict.txt","a",encoding="utf-8") as disdict:
					disdict.write("%s\n" %self.dis)
			
				
			jieba.load_userdict("lib/mydict.txt")
			with open("lib/stopwords.txt",encoding='utf-8') as stopwordsfile:
				for line in stopwordsfile:
					line=line.strip('\n').strip()
					stopwords.append(line)

			with open(filepath, 'r',encoding='utf-8') as wbfile:
				for line in wbfile:
					wb=line.strip('\n').strip()
					wbtext=wb
					keywords_iterator=jieba.analyse.extract_tags(wbtext, topK=30, withWeight=False, allowPOS=('a','nr','ns','nt','nz','n', 'vn', 'v', 't') )
					wbwords = [key for key in keywords_iterator if key not in stopwords]
					if wbwords:
						keywords.append(wbwords)
						decribe.append(wbtext)

			info={}
			info["text"]=keywords
			info["decribe"]=decribe
			self.keywords=info["text"]
			self.decribe=info["decribe"]
			pickle.dump(info,open(newfile,"wb"))

	def concurrence(self):
		concurrence={}
		for wbwords in self.keywords:
				for i in range(len(wbwords)):
						for j in range(i+1,len(wbwords)):
								keypair=[wbwords[i],wbwords[j]]
								keypair.sort()
								keypair=tuple(keypair)
								if keypair not in concurrence.keys():
										concurrence[keypair]=1
								else:
										concurrence[keypair]=concurrence[keypair]+1
		self.concurrence=concurrence
		#print(len(concurrence.keys()))


	def mean_edge(self):
		mean_edge=(float)(sum(self.concurrence.values()))/(float)(len(self.concurrence))
		return mean_edge
		
	def median_edge(self):
		mlist=list(self.concurrence.values())
		n=len(mlist)
		mlist=sorted(mlist)
		if n%2==0:
			x=mlist[round(n/2)]+mlist[round(n/2)+1]
			median_edge=round(x/2)
		else:
			median_edge=mlist[round(n/2)]
		return median_edge
		
	def remove_edge(self,thresh):
		pairs=list(self.concurrence.keys())
		for pair in pairs:
				if self.concurrence[pair]<thresh:
						del self.concurrence[pair]
		#print(len(self.concurrence.keys()))


	def multi_graph_construct(self):
		import networkx as nx
		pairs=self.concurrence.keys()
		#print(pairs)
		nodes=set()
		for pair in pairs:
				nodes.add(pair[0])
				nodes.add(pair[1])
		
		G=nx.MultiGraph()
		G.add_nodes_from(nodes)
		
		for pair in pairs:
				for t in range(self.concurrence[pair]):
						G.add_edge(pair[0],pair[1])
		
		return G  

	def find_cliques(self,g):
		import networkx as nx
		nodes=g.nodes()

		G=nx.Graph()
		G.add_nodes_from(nodes)
		
		for item1 in nodes:
			for item2 in nodes:

				if not item1==item2:
					if g.number_of_edges(item1, item2):
						G.add_edge(item1, item2)
		cliques=[item for item in list(nx.find_cliques(G)) if len(item)>=3]
	
		checked_clique=[]#一个clique中的所有节点在一句话出现
		for cl in cliques:
			flag=False
			for item in self.keywords:
				occur=0
				for word in cl:
					if word in item:
						occur=occur+1

				if occur==len(cl):
					flag=True
			if flag:
				checked_clique.append(cl)
				#print(cl)


		return checked_clique





		




		
				

				
				
