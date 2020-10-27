import pandas as pd
import matplotlib

import os

try:
    import venn
except ImportError:
    print("Trying to Install required module: venn\n")
    os.system("python -m pip install venn")
    import venn

df = pd.read_excel("binary_subject_areas.xlsx")

sa = ["Health Sciences", "Life Sciences", "Physical Sciences", "Social Sciences & Humanities"]
df["Science"] = df[sa].astype(str).apply(lambda x: ''.join(x), axis=1)
labels = df["Science"].value_counts().to_dict()
labels["1111"] += df["Multidisciplinary"].sum()

sa_counts = df[sa].sum().to_list() 
names = [sa[i] + " (%d)" % (sa_counts[i]+labels["1111"]) for i in range(4)] 

matplotlib.use("Agg")

fig, ax = venn.venn4(labels, names=names)
fig.savefig("venn.png")

# change to colors from the paper
#fig, ax = venn.venn4(labels, names=names, colors=[[90/255., 155/255., 212/255., 0.5],[92/255., 192/255., 98/255., 0.5],[246/255., 236/255., 86/255., 0.6],[241/255., 90/255., 96/255., 0.4]], dpi=300)
#fig.savefig("venn.png")