import pandas as pd
import glob

path = r'SalesAnalysis/Sales_Data'
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv('SalesAnalysis/Output/output_data.csv',index=False)