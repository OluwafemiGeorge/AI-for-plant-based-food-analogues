# -*- coding: utf-8 -*-
"""functionalGrpPlot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m62wgyTXVPYHHLTrgLv_kf2a2AlAXII0
"""

from google.colab import drive
drive.mount('/content/drive')

cd 'drive/MyDrive/Colab Notebooks'

#!/usr/bin/env python3
!pip install rdkit-pypi
import time
import random
import sys
from pathlib import Path
import seaborn as sns

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rdkit import Chem
from rdkit import DataStructs
from rdkit.ML.Cluster import Butina
from rdkit.Chem import Draw
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Draw import SimilarityMaps
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from statistics import mean

import time
start_time = time.time()
# read and Concatenate the csv's
df = pd.read_csv('single_functional_group.csv')

code = []
for i in range(len(df)):
  code.append("A{0}".format(i+1))
df['code'] = code
code=list(df['code'])
df = df.dropna()
df

# df = df.sample(n=9000, random_state=1)
# df =df.dropna()
# df = df.sample(n=9000, random_state=1)

# proof and make a list of SMILES
df_smiles = df['SMILES']
c_smiles = []
total_invalid = 0
for ds in df_smiles:
    try:
        cs = Chem.CanonSmiles(ds)
        c_smiles.append(cs)
    except:
        total_invalid += 1
        print('Invalid SMILES:', ds)
print(total_invalid)

from statistics import mean
# make a list of mols
ms = [Chem.MolFromSmiles(x) for x in c_smiles]
mms = [k for k in c_smiles]
r=[]
for i in mms:
  mol=Chem.MolFromSmiles(i)
  maccs = MACCSkeys.GenMACCSKeys(mol)
  array = np.zeros((0,), dtype=np.int8)
  p_maccs= np.nonzero(maccs)
  q_maccs=np.array(p_maccs)
  w_maccs=q_maccs.size
  r.append(w_maccs)
df1 = pd.DataFrame({'nonzero':r})
 #make a list of mols
ms = [Chem.MolFromSmiles(x) for x in c_smiles]
mms = [k for k in c_smiles]
df1=list(df1['nonzero'])

# make a list of fingerprints (fp)
rdkit_gen = rdFingerprintGenerator.GetRDKitFPGenerator(maxPath=7)
fps_maccs = [MACCSkeys.GenMACCSKeys(x) for x in ms]

# the list for the dataframe
ta, sim, bits, new_diff = [], [], [], []

from numpy.lib.index_tricks import s_

#for just 1st two
n_maccs = len(fps_maccs) # 1st two
#s = tanimoto coefficient
s_maccs = DataStructs.BulkTanimotoSimilarity(fps_maccs[0], fps_maccs[:] ) # +1 compare with the next to the last fp
for m in range(len(s_maccs)):
    ta.append(code[:][m])
    sim.append(s_maccs[m])
    new_diff.append(1 - s_maccs[m])
bits = df1
print(len(ta), len(sim), len(new_diff), len(bits))

# build the dataframe and sort it}
d = {'target':ta, 'Similarity':sim, 'No_of_bits':bits, 'new_diff':new_diff}
df_final = pd.DataFrame(data=d)
df_final

# make a list of fingerprints (fp)
rdkit_gen = rdFingerprintGenerator.GetRDKitFPGenerator(maxPath=7)
fps_maccs = [MACCSkeys.GenMACCSKeys(x) for x in ms]
fps_m512 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=512) for mol in ms]
fps_m1024 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024) for mol in ms]
fps_m2048 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048) for mol in ms]
fps_m4096 = [AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=4096) for mol in ms]
print(fps_maccs)

single_functional_group = pd.read_csv('single_functional_group.csv')
# single_functional_group= single_functional_group.dropna()
single_functional_group['Functional_group'].unique()

from numpy.lib.index_tricks import s_
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()

# print()

#for just 1st two
n_maccs = len(fps_maccs) # 1st two
n_m512 = len(fps_m512)
n_m1024 = len(fps_m1024)
n_m2048 = len(fps_m2048)
n_m4096 = len(fps_m4096)
#tanimoto coefficient
s_maccs = DataStructs.BulkTanimotoSimilarity(fps_maccs[0], fps_maccs[:] ) # +1 compare with the next to the last fp
s_m512 = DataStructs.BulkTanimotoSimilarity(fps_m512[0], fps_m512[:] )
s_m1024 = DataStructs.BulkTanimotoSimilarity(fps_m1024[0], fps_m1024[:] )
s_m2048 = DataStructs.BulkTanimotoSimilarity(fps_m2048[0], fps_m2048[:] )
s_m4096 = DataStructs.BulkTanimotoSimilarity(fps_m4096[0], fps_m4096[:] )
ns_maccs = []
ns_m512 = []
ns_m1024 = []
ns_m2048 = []
ns_m4096 = []
for i in s_maccs:
  ns_maccs.append(1 - i)
for i in s_m512:
  ns_m512.append(1 - i)
for i in s_m1024:
  ns_m1024.append(1 - i)
for i in s_m2048:
  ns_m2048.append(1 - i)
for i in s_m4096:
  ns_m4096.append(1 - i)
print(ns_maccs)
print(ns_m512)
print(ns_m1024)
print(ns_m2048)
print(ns_m4096)
class_arr = []
# counter = 1
# for unique_functional_group in single_functional_group['Functional_group'].unique():
#   for functional_group in single_functional_group['Functional_group']:
#     if unique_functional_group == functional_group:



for i in s_m4096:
  if i <= 0.05:
      classification = "Alkane"
      class_arr.append(classification)
  elif i <= 0.1:
    classification = "Alkene"
    class_arr.append(classification)
  elif i <= 0.15:
    classification = "Alkyne"
    class_arr.append(classification)
  elif i <= 0.2:
    classification = "Aromatic hydrocarbon"
    class_arr.append(classification)
  elif i <= 0.25:
    classification = "Halide"
    class_arr.append(classification)
  elif i <= 0.3:
    classification = "Alcohol"
    class_arr.append(classification)
  elif i <= 0.35:
    classification = "Aldehyde"
    class_arr.append(classification)
  elif i <= 0.5:
    classification = "carbonyl compounds"
    class_arr.append(classification)
  elif i <= 0.6:
    classification = "Ether"
    class_arr.append(classification)
  elif i <= 0.7:
    classification = "Thiol"
    class_arr.append(classification)
  elif i <= 1:
    classification = "Nitrate group"
    class_arr.append(classification)
  # elif i <= 0.6:
  #   classification = "12"
  #   class_arr.append(classification)
  # # elif i <= 0.65:
  #   classification = "13"
  #   class_arr.append(classification)
  # elif i <= 0.7:
  #   classification = "14"
  #   class_arr.append(classification)
  # elif i <= 0.75:
  #   classification = "15"
  #   class_arr.append(classification)
  # elif i <= 0.8:
  #   classification = "16"
  #   class_arr.append(classification)
  # elif i <= 0.85:
  #   classification = "17"
  #   class_arr.append(classification)
  # elif i <= 0.9:
  #   classification = "18"
  #   class_arr.append(classification)
  # elif i <= 0.95:
  #   classification = "19"
  #   class_arr.append(classification)
  # elif i <= 1:
  #   classification = "20"
  #   class_arr.append(classification)
d = {'maccs':ns_maccs, 's_m512':ns_m512, 's_m1024':ns_m1024, 's_m2048':ns_m2048, 's_m4096':ns_m4096, 'classification':class_arr}
df_final = pd.DataFrame(data=d)
df_final["classification_enc"] = enc.fit_transform(df_final['classification'])
print(df_final)
df_final.to_csv('tanimoto_coef.csv', index=False, sep=',')

df_final["classification"].value_counts()

#reading the file
df=pd.read_csv('tanimoto_coef.csv')
df1=pd.read_csv('tanimoto_coef.csv')
df.drop(['classification'], axis=1, inplace=True)
features=df.keys()
print(df.head())

# Separating out the features
x = df.loc[:, features].values
x.shape

#Scatter plot for visualization
plt.scatter(x[:,0], x[:,1]);

# Commented out IPython magic to ensure Python compatibility.
from __future__ import print_function
import time
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from sklearn.datasets import load_iris
from pandas.plotting import scatter_matrix

plt.figure(figsize = (20,10))
plt.subplots_adjust(top = 1.5)


for index, p in enumerate([5, 10, 30, 50]):
    labels = df_final.classification.unique().tolist()
    colors = ['Blue', 'Green', 'Purple', 'Red', 'Orange', 'gray', 'yellow', "brown", "pink", "indigo", "black"]#, "hot"]
    tsne = TSNE(n_components=2, perplexity =p, random_state = 0, learning_rate=100)
    # data_2d =tsne.fit_transform(x)
    data_2d=pd.DataFrame(data_2d, columns=['tsne1', 'tsne2'])
    plt.subplot(2,2,index+1)
    handles = plt.scatter(data_2d['tsne1'], data_2d['tsne2'], c=df_final.classification_enc, cmap=matplotlib.colors.ListedColormap(colors))
    plt.title('Perplexity = '+ str(p))
    plt.legend(handles=handles.legend_elements()[0], labels=labels)

plt.show()

]#You will use the sklearn library to import the PCA module
from sklearn.decomposition import PCA
pca_sim = PCA(n_components=2)
principalComponents_sim = pca_sim.fit_transform(x)

#Next, let's create a DataFrame that will have the principal component values for all 10,000 samples.
principal_sim_Df = pd.DataFrame(data = principalComponents_sim
             , columns = ['principal component 1', 'principal component 2'])
principal_sim_Df.tail()

import seaborn as sns
plt.figure(figsize=(8,8))
sns.scatterplot(
    x="principal component 1", y="principal component 2",
    data=principal_sim_Df,
    legend='full',
    s=50, c=df_final.classification)

tsne = TSNE(n_components=2, perplexity = 300, random_state = 0)
data_2d =tsne.fit_transform(x)
plt.scatter(data_2d[:,0], data_2d[:,1]);

