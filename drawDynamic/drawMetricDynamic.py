from author_cooperation import author_nx
from citation import cal_citation
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from functools import cmp_to_key
basedir="../2022-"


def randomgraph_generation(k,node_num,edge_num):
    # k=[]
    # return nx.erdos_renyi_graph(node_num,2*edge_num/(node_num*(node_num-1)))

    return nx.watts_strogatz_graph(node_num,k,2*edge_num/(node_num*(node_num-1)))
#排序算法，优先按effective_size降序排序，然后按照citation进行降序排序
def custom_sorted(x,y):
    if x[1]["effective_size"]>y[1]["effective_size"]:
        return 1
    elif x[1]["effective_size"]<y[1]["effective_size"]:
        return -1
    else:
        if  x[1]["citation"] > y[1]["citation"]:
            return 1
        elif x[1]["citation"] < y[1]["citation"]:
            return -1
        else:
            return 0

def drawPaper():
    paper_num_lst=[]
    fig, ax = plt.subplots()
    for i in range(1,12):
        if i < 10:
            filename = basedir + '0' + str(
                i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0' + str(i) + '_final.json'
        else:
            filename = basedir + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-' + str(i) + '_final.json'
        tarfile = open(filename, 'r')
        tar_str=tarfile.read()
        lst=tar_str.split("---------------------------------\n")
        paper_num_lst.append(len(lst))
    plt.plot(range(1,12),paper_num_lst,color="red",linestyle='--')
    ax.set_ylim(0,250)
    ax.set_xlabel("Month",fontsize=18)
    ax.set_ylabel("Paper number",fontsize=18)
    plt.savefig("paper_num.png")
    plt.show()

def drawCandidateAuthor(candidate_lst):
    all_effective_size=[]
    candidate_effective_size_dict={}
    for candadite in candidate_lst:
        candidate_effective_size_dict[candadite] = []
    for i in range(1,12):
        if i<10:
            filename=basedir+'0'+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor2022-0'+str(i)+'.json'
        else:
            filename=basedir+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor2022-'+str(i)+'.json'
        tarfile=open(filename,'r')
        res_dict = author_nx.author_analysis_pipeline(filename, None)
        effective_size_res=res_dict["effective_size_res"]

        for candidate in candidate_lst:
            candidate_effective_size_dict[candidate].append(effective_size_res[candidate])

        tarfile.close()
    plt.figure()
    fig,ax=plt.subplots()
    for candidate in candidate_lst:
        plt.plot(range(1,12),candidate_effective_size_dict[candidate],label=candidate)

    ax.set_xlabel("Month",fontsize=18)
    ax.set_ylabel("effectivesize",fontsize=18)
    ax.set_title('effective_size',fontsize=18)
    ax.legend()
    plt.savefig("candidateEffectivesize.png")

    plt.show()
def drawCitation():
    citation_lst=[]
    for i in range(1,12):
        if i<10:
            filename=basedir+'0'+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0'+str(i)+'_final.json'
        else:
            filename=basedir+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-'+str(i)+'_final.json'
        tarfile=open(filename,'r')

        top_publisher,citation,avg_citation_foreach_publisher_lst=cal_citation.citation_analysis_pipeline(filename,None)
        # for k in effective_size_res.keys():
        #     print(k)
        top10=sorted(citation,reverse=True)[:10]
        print("toop10:",top10)
        citation_lst.append(top10)
        tarfile.close()
    np.random.seed(19680801)

    labels = [str(i) for i in range(1, 12)]
    fig, ax1 = plt.subplots(figsize=(9, 4))
    # rectangular box plot

    bplot1 = ax1.boxplot(citation_lst,
                         showmeans=True,
                         flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 10},
                         meanprops={"marker": "*", 'color': 'g', 'linewidth': 1.5},
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
    ax1.set_title('Citation box plot')

    # fill with colors
    colors = ['Honeydew', 'Ivory', 'LemonChiffon', 'PaleTurquoise', 'LavenderBlush',
              'AliceBlue', 'LightCyan', 'PaleTurquoise', 'Lavender', 'PowderBlue', 'AliceBlue']
    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)

    # adding horizontal grid lines
    for ax in [ax1]:
        ax.yaxis.grid(True)
        ax.set_xlabel('Month',fontsize=18)
        ax.set_ylabel('Citation',fontsize=18)
    plt.savefig("citation.png")

    plt.show()
def drawLCC():
    eff_lst = []
    LCC_lst = []
    for i in range(1,12):
        if i < 10:
            filename = basedir + '0' + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0' + str(i) + '_final.json'
        else:
            filename = basedir + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-' + str(i) + '_final.json'
        tarfile=open(filename,'r')
        res_dict=author_nx.author_analysis_pipeline(filename,None)
        effective_size_res=res_dict["effective_size_res"]
        LCC_size=res_dict["LCC_size"]
        node_size=res_dict["nodes"]
        LCC_size/=node_size
        avg_eff=0

        # for k in effective_size_res.keys():
        #     print(k)
        top10=sorted(list(effective_size_res.values()),reverse=True)[:10]
        print("top10:",top10)
        for v in top10:
            avg_eff+=v
        avg_eff/=10

        eff_lst.append(avg_eff)

        LCC_lst.append(LCC_size)

        tarfile.close()

    x = np.arange(1,12)
    y = LCC_lst
    fig, ax = plt.subplots()
    ax.plot(x, y,color="black",linewidth=3)
    ax.set_ylim(0,1)
    ax.set_xlabel("Month",fontsize=18)
    ax.set_ylabel("The fraction of LCC",fontsize=18)
    # plt.legend(loc='lower right')
    plt.savefig("LCC.png")
    plt.show()
def drawAverageCluster():
    random_cluster_coefficient_lst=[]
    cluster_coefficient_lst = []
    k=[0,5,5,5,5,5,5,5,5,6,6,6]
    for i in range(1,12):

        if i<10:
            filename=basedir+'0'+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0'+str(i)+'_final.json'
        else:
            filename=basedir+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-'+str(i)+'_final.json'
        tarfile=open(filename,'r')
        res_dict = author_nx.author_analysis_pipeline(filename, None)
        random_graph = randomgraph_generation(k[i],res_dict["nodes"], res_dict["edges"])
        random_graph_cluster_coefficient=nx.average_clustering(random_graph)
        print("random_graph_cluster_coefficient:",random_graph_cluster_coefficient)
        cluster_coefficient = res_dict["cluster_coefficient"]
        random_cluster_coefficient_lst.append(random_graph_cluster_coefficient)
        cluster_coefficient_lst.append(cluster_coefficient)
        tarfile.close()
    fig, ax = plt.subplots()
    ax.plot(range(1, 12), cluster_coefficient_lst, color="black", linewidth=3, linestyle="--", label='Our network')
    ax.plot(range(1, 12), random_cluster_coefficient_lst, color="red", linewidth=3, linestyle="-", label='Small-world network')
    ax.set_xlabel('Month',fontsize=18)
    ax.set_ylabel('cluster coefficient',fontsize=18)
    ax.set_ylim(0,1)
    ax.legend()
    plt.savefig("cluster_coefficient.png")
    plt.show()
def drawNodeAndEdge():
    node_lst=[]
    edge_lst=[]
    for i in range(1,12):
        if i < 10:
            filename = basedir + '0' + str(
                i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0' + str(i) + '_final.json'
        else:
            filename = basedir + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-' + str(i) + '_final.json'
        tarfile=open(filename,'r')
        res_dict = author_nx.author_analysis_pipeline(filename, None)
        node_num=res_dict["nodes"]
        edge_num=res_dict["edges"]
        node_lst.append(node_num)
        edge_lst.append(edge_num)
        tarfile.close()
    fig, ax = plt.subplots()
    ax.plot(range(1,12),node_lst,color="blue", linewidth=2,linestyle="--",label='nodes')
    ax.plot(range(1,12),edge_lst,color="red",linewidth=2,linestyle="-",label='edges')
    ax.set_xlabel('Month',fontsize=18)
    ax.set_ylabel('Number',fontsize=18)
    ax.legend()
    plt.savefig("node&edge.png")
    plt.show()


def drawEffectiveSize():
    eff_lst=[]
    avg_lst=[]
    for i in range(1,12):
        if i < 10:
            filename = basedir + '0' + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0' + str(i) + '_final.json'
        else:
            filename = basedir + str(i) + '/' + 'fourpublisher_arxiv_withsource_updatedauthor_citation2022-' + str(i) + '_final.json'
        tarfile=open(filename,'r')
        res_dict=author_nx.author_analysis_pipeline(filename,None)
        effective_size_res=res_dict["effective_size_res"]
        LCC_size=res_dict["LCC_size"]
        avg_eff=0

        # for k in effective_size_res.keys():
        #     print(k)
        top10=sorted(list(effective_size_res.values()),reverse=True)[:10]
        for k in top10:
            avg_eff+=k

        avg_eff/=10
        avg_lst.append(avg_eff)


        eff_lst.append(top10)


        tarfile.close()
    # print("avg_lst:",avg_lst)
    # Random test data
    np.random.seed(19680801)

    labels = [str(i) for i in range(1,12)]
    print("labels:",labels)
    print("lst:",eff_lst,len(eff_lst))
    # fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
    fig, ax1 = plt.subplots(figsize=(9, 6))
    # rectangular box plot
    bplot1 = ax1.boxplot(eff_lst,
                         showmeans=True,
                         flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 10},
                         meanprops={"marker":"*",'color': 'g', 'linewidth': 1.5},
                         vert=True,  # vertical box alignment
                         patch_artist=True,  # fill with color
                         labels=labels)  # will be used to label x-ticks
    # ax1.set_title('Effectivesize box plot')

    # fill with colors
    colors = ['Honeydew', 'Ivory', 'LemonChiffon','PaleTurquoise','LavenderBlush',
              'AliceBlue','LightCyan','PaleTurquoise','Lavender','PowderBlue','AliceBlue']
    for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)

    # adding horizontal grid lines
    for ax in [ax1]:
        ax.yaxis.grid(True)
        ax.set_xlabel('Month',fontsize=18)
        ax.set_ylabel('Effectivesize',fontsize=18)
    plt.savefig("effectivesize.png")
    plt.show()

def hat_graph(ax, xlabels, values, group_labels):
    """
    Create a hat graph.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Axes to plot into.
    xlabels : list of str
        The category names to be displayed on the x-axis.
    values : (M, N) array-like
        The data values.
        Rows are the groups (len(group_labels) == M).
        Columns are the categories (len(xlabels) == N).
    group_labels : list of str
        The group labels displayed in the legend.
    """

    def label_bars(heights, rects):
        """Attach a text label on top of each bar."""
        for height, rect in zip(heights, rects):
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),  # 4 points vertical offset.
                        textcoords='offset points',
                        ha='center', va='bottom')

    values = np.asarray(values)
    x = np.arange(values.shape[1])
    ax.set_xticks(x)
    spacing = 0.3  # spacing between hat groups
    width = (1 - spacing) / values.shape[0]
    heights0 = values[0]
    for i, (heights, group_label) in enumerate(zip(values, group_labels)):
        style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
        rects = ax.bar(x - spacing/2 + i * width, heights - heights0,
                       width, bottom=heights0, label=group_label, **style)
        label_bars(heights, rects)

def drawEffectiveAndCitation():
    avg_eff_lst = []
    avg_cit_lst = []

    for i in range(1,12):
        if i<10:
            filename=basedir+'0'+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-0'+str(i)+'.json'
        else:
            filename=basedir+str(i)+'/'+'fourpublisher_arxiv_withsource_updatedauthor_citation2022-'+str(i)+'.json'

        res_dict = author_nx.author_analysis_pipeline(filename, None)
        author_citation_perform=res_dict["author_citation_perform"]

        avg_eff=0
        avg_cit=0
        author_citation_perform=sorted(list(author_citation_perform.items()),reverse=True,key=cmp_to_key(custom_sorted))[:10]
        print("author_citation_perform:",author_citation_perform)
        for item in author_citation_perform:
            avg_eff+=item[1]["effective_size"]
            avg_cit+=item[1]["citation"]
            # eff_lst.append(item[1]["effective_size"])
            # cit_lst.append(item[1]["citation"])
        avg_eff/=10
        avg_cit/=10
        avg_eff_lst.append(avg_eff)
        avg_cit_lst.append(avg_cit)
    return avg_eff_lst,avg_cit_lst


if __name__ == "__main__":
    candidate_lst=['Hideyuki Kanematsu', 'Dusit Niyato', 'Chunyan Miao', 'Zehui Xiong', 'Lik-Hang Lee']
    # drawEffectiveSize()
    # drawNodeAndEdge()

    drawAverageCluster()
    # drawPaper()
    # drawLCC()
    # drawCandidateAuthor(candidate_lst)
    # drawCitation()
    # initialise labels and a numpy array make sure you have
    # N labels of N number of values in the array
    # avg_eff_lst,avg_cit_lst=drawEffectiveAndCitation()

    # print("avf_cit:",avg_cit_lst)
    # fig, ax = plt.subplots()
    # ax2 = ax.twinx()
    # fruits = range(1,12)
    # counts = avg_cit_lst
    #
    # bar_colors = ['Honeydew', 'Ivory', 'LemonChiffon','PaleTurquoise','LavenderBlush',
    #           'AliceBlue','LightCyan','PaleTurquoise','Lavender','PowderBlue','AliceBlue']
    #
    # ax.bar(fruits, counts,  color=bar_colors)
    # ax2.plot(fruits, avg_eff_lst, color="blue", linewidth=2,linestyle="--",label='effectiveSize')
    # ax.set_ylabel('citation')
    # ax2.set_ylabel('effectivesize&')
    # ax.set_title('effectivesize&citation')
    # plt.show()