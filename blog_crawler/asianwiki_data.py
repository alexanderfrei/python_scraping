import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
from sklearn import preprocessing

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# interesting_files = glob.glob("*.csv")
# df = pd.DataFrame()
# for filename in sorted(interesting_files):
#     df = pd.concat([df, pd.read_csv(filename, sep=';', header=None)])
# df.to_csv('comedy.csv',mode='w', sep=";")

df = pd.read_csv("comedy.csv", sep=';', header=None)
df.drop_duplicates()
df = df.iloc[:,1:]
df = df.dropna(subset=[1,2])
df = df.assign(val = pd.Series(np.sqrt(df[1].astype(float) * df[2])))

df[(df[2] > 10) & (df[1].astype(float) > 75)].sort_values('val', ascending=[0]).loc[:,[3,'val',1,2,3,4,5,6]].\
    to_csv("top.csv", header=None, index=None, sep=';', mode='w')

#
# plt.hist(df.loc[:,'val'], bins=50, range=(0,1000))
# plt.show()

