import  pandas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
plt.rcParams["font.size"]=18
data=pd.read_excel("corr.xlsx")
# df=data.iloc[:20,:]
# pandas.DataFrame().corr(method="kendall")
X=data['citation']
Y=data["effective_size"]
res1=np.corrcoef(X,Y)
# print("res1:",res1)
res=data[["citation","effective_size"]].corr()
print("res:",res)
fig,ax=plt.subplots(figsize=(5,5))
sns.set_style("whitegrid")

sns.heatmap(res,square=True,annot=True,cmap="Blues_r")
# plt.imshow()
# plt.tight_layout()
# plt.colorbar()
# l1=["effective_size"]
# l2=["citation"]
# plt.xticks(np.arange(len(l1)),labels="effective_size")
# plt.yticks(np.arange(len(l2)),labels="citation")
plt.savefig("pearson.png")
plt.show()


pd.plotting.scatter_matrix(data)

plt.show()
