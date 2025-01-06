# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 15:58:22 2025

@author: JMKIR
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
f = r"C:\Users\jmkir\Ramboll\JMKIR - Documents\personalWebpage\foundationResponse\ML\dataFile_foundationWidth_effect.json"
df = pd.read_json(f)
ax, fig = plt.subplots(figsize=(12,8))
sns.scatterplot(data=df, x='foundationWidth',y='Uy')