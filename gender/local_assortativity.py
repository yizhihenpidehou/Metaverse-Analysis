import json

import easygraph as eg
import numpy as np
import matplotlib.pyplot as plt

def cal_local_assortativity(inputpath,respath):
    with open(inputpath,'r') as ff:
        G=eg.Graph()
        ff_str=ff.read()
        lst=ff_str.split("---------------------------------\n")
        for i in range(0,len(lst)-1):
            json_str=json.loads(lst[i])
            gender=json_str["gender"]
            author_lst=json_str["author"]
            for j in range(0,len(author_lst)):
                for z in range(j,len(author_lst)):
                    if G.has_node(author_lst[j]) == False:
                        G.add_node(author_lst[j],gender=gender[j])

                    if G.has_node(author_lst[z]) == False:
                        G.add_node(author_lst[z], gender=gender[z])

                    if G.has_edge(author_lst[j],author_lst[z]) == False:
                        G.add_edge(author_lst[j],author_lst[z])

        G_=eg.convert_node_labels_to_integers(G)
        print(G.nodes,G_.nodes)
        edgelist=[[edge[0],edge[1]] for edge in G_.edges]

        # print("edgelist:",edgelist)
        nodes_label=[]
        for node in G_.nodes:
            # print("node:",node)
            nodes_label.append(G_.nodes[node]["gender"])
        # metaverse_author_file=open("metaverse_author_edges.txt",'w')
        metaverse_author_labels=open(respath+"metaverse_author_labels.txt",'w')
        # for edge in edgelist:
        #     metaverse_author_file.write(edgelist)
        eg.write_edgelist(G_,respath+"metaverse_author_edges.txt",data=False)
        for l in nodes_label:
            metaverse_author_labels.write(str(l)+'\n')
        metaverse_author_labels.close()
        edgelist=np.int32(edgelist)
        nodes_label=np.int32(nodes_label)
        assortM, assortT, Z=eg.localAssort(edgelist=edgelist,node_attr=nodes_label)
        print("assortT:",assortT)
        # weights = np.ones_like(assortT) / float(len(assortT))
        plt.ylim(0,2.5)
        plt.hist(assortT,color="green",density=True)

        plt.xlabel("local assortativity")
        plt.ylabel("frequency")
        plt.savefig(respath)
        plt.show()


def local_assortativity_pipleline(inputpath,respath):
    cal_local_assortativity(inputpath=inputpath, respath=respath)
    return respath
# if __name__ == '__main__':
#     baseurl = '/Users/yizhihenpidehou/Desktop/fdu/Metaverse-Analysis/'
#
#     for i in range(1, 12):
#         targeturl = baseurl
#         dirurl = baseurl
#         resurl=baseurl
#         if i < 10:
#             targeturl += "2022-0" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-0" + str(i) + "_withgender.json"
#             dirurl+="2022-0" + str(i)+'/'
#         else:
#             targeturl += "2022-" + str(i) + "/fourpublisher_arxiv_withsource_updatedauthor2022-" + str(i) + "_withgender.json"
#             dirurl += "2022-" + str(i) + '/'
#
#         request_file = open(targeturl, 'r')
#         request_file_str = request_file.read()
#         request_file_lst = request_file_str.split("---------------------------------\n")
#         cal_local_assortativity(inputpath=targeturl,respath=dirurl,month=i)