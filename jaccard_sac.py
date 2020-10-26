import pandas as pd
import scipy.spatial.distance as sd
import numpy as np

import scipy.spatial as sp, scipy.cluster.hierarchy as hc

import seaborn as sns
from matplotlib import pyplot as plt

# The dataset has to include binary variables SAC = ...
# which indicate if a document is classified to a particular SAC
df = pd.read_excel("binary_sac.xlsx")

df = df[[x for x in df.columns if ("SAC =" in x and "Multi" not in x)]]
# exclude other irrelevant variables for this analysis

names = [x.split("= ")[1] for x in df.columns]
d_names = dict([(i, names[i]) for i in range(len(names))])

df_np0 = np.array(df)

def get_matrix(df_np, f=sd.jaccard):
    nc = df_np.shape[1]
    mat = np.zeros((nc, nc))
    for i in range(nc):
        for j in range(i, nc):
            coeff = f(df_np[:,i], df_np[:,j])
            mat[i, j], mat[j, i] = 1-coeff, 1-coeff
    return mat

# first compute the order of SACs

mat0 = get_matrix(df_np0)
linkage = hc.linkage(sp.distance.squareform(1-mat0), method="ward")
cm0 = sns.clustermap(1-mat0, row_linkage=linkage, col_linkage=linkage)

# perm - permuted order of SACs
perm = cm0.data2d.index.tolist()

perm_names = ["SAC = " + d_names[p] for p in perm]
p_names = [d_names[p] for p in perm]
df = df[perm_names]

df_np = np.array(df)

f, ax = plt.subplots(figsize=(20,20), facecolor='w', edgecolor='k')

mat = get_matrix(df_np)

linkage = hc.linkage(sp.distance.squareform(1-mat), method="ward")
mask = (np.tril(1-mat)==0)
cm = sns.clustermap(1-mat, mask=mask, row_linkage=linkage, col_linkage=linkage, row_cluster=False, vmin=0.5, vmax=1.0, annot=True, fmt='.2f', annot_kws={"fontsize":5}, xticklabels=p_names, yticklabels=p_names, cbar_kws={"shrink": .82})

ax = cm.ax_heatmap
bx = ax.twinx()
bx.set_yticklabels([]) 

ax.axhline(y=0, color='k',linewidth=2)
ax.axhline(y=mat.shape[1], color='k',linewidth=2)
ax.axvline(x=0, color='k',linewidth=2)
ax.axvline(x=mat.shape[0], color='k',linewidth=2)

plt.savefig("jaccard.png", dpi=300, bbox_inches = "tight")