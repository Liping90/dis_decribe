def process(file):
    import datetime
    topics=[]
    topic_time=[]
    with open(file,encoding="utf-8") as f:
        for line in f:
            line=line.strip('\n').strip()
            if line[0:10]=='*'*10:
                name=line[line.index(":")+1:].strip()
                name=name[0:name.index("*")]
                #print(name)
                topics.append(name)
                topic_time.append([])
                
            elif len(line)==16 and line[0:3]=="201":
                #print(line)
                time=datetime.datetime.strptime(line.strip()[0:10], "%Y-%m-%d")
                topic_time[-1].append(time)
                
    return topics,topic_time
                    
def plot(topic,x,y,cusum,i,movie):
    import pylab
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime
    pylab.mpl.rcParams['font.sans-serif'] = ['SimHei']
    pylab.mpl.rcParams['axes.unicode_minus'] = False
    
    fig, axes = plt.subplots()
    axes.plot(x, cusum, 'k--',label="Cumsum")
    axes.plot(x, y, 'b',label="Trend")
    axes.set_xlabel('dates')
    axes.grid(True)
    fig.autofmt_xdate()
    legend = axes.legend(loc='upper left', shadow=True, ncol=1)
    plt.title("%s" %(' '.join(topic)) )
    plt.savefig("figures/%s-%s.png" %(movie,i))

def cusum(topics,topic_time,topk,movie):
    count=[len(each) for each in topic_time]
    total=len(count)
    #print(count)
    top=list(zip(count,range(total)))
    top.sort(reverse=True)
    #print(top)
    for i in range(topk):
        topic=topics[top[i][1]]
        time=topic_time[top[i][1]]

        x=sorted(list(set(time)))
        y=[0]*len(x)
        for each in time:
            y[x.index(each)]+=1
        t=sum(y)
        y=[each/t for each in y]
        cusum=[0]*len(x)
        for j in range(len(y)):
            cusum[j]=sum(y[0:j+1])
        plot(topic,x,y,cusum,i,movie)      
