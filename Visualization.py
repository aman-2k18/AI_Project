import matplotlib
import pandas as pd
import numpy as np

url1 = 'https://raw.githubusercontent.com/aman-2k18/AI_Project/main/hillClimbing_resultData.txt?token=ANPGBX2QKV4MVEX6Y2RV6YC7W2K7I'
url2 = 'https://raw.githubusercontent.com/aman-2k18/AI_Project/main/randomRestart_resultData.txt?token=ANPGBX6G3DYHBYWDW5YJX627W7ZM4'
url3 = 'https://raw.githubusercontent.com/aman-2k18/AI_Project/main/simulatedAnnealing_resultData.txt?token=ANPGBXYUBTGSVH6PCGLGH7K7W7ZOQ'
df1 = pd.read_csv(url1, sep="\t")
df2 = pd.read_csv(url2, sep="\t")
df3 = pd.read_csv(url3, sep="\t")

data = {'avgtime_Hill':  [],
        'avgtime_Res': [],
        'avgtime_Sim': []
        }

df = pd.DataFrame (data, columns = ['N','avgtime_Hill','avgtime_Res','avgtime_Sim'])

df['N'] = df1['N']

df['avgtime_Hill'] = np.log(df1[' avgTime'])

df['avgtime_Res'] = np.log(df2[' avgTime'])

df['avgtime_Sim'] = np.log(df3[' avgTime'])

dfa = pd.DataFrame (data, columns = ['N','successRate_Hill','successRate_Res','successRate_Sim'])
dfa['N'] = df1['N']
dfa['successRate_Hill'] = (df1[' successRate'])

dfa['successRate_Res'] = (df2[' successRate'])

dfa['successRate_Sim'] = (df3[' successRate'])


df = df.set_index('N')
dfa = dfa.set_index('N')
print(df)
print(dfa)
lines = df.plot.line( grid=True, marker="o",ylabel="Time (secs) - log Scale", color={"avgtime_Hill": "red", "avgtime_Res": "blue", 'avgtime_Sim': '#742802'})

lines = dfa.plot.line( grid=True, marker="o",ylabel="Success Rate", color={"successRate_Hill": "red", "successRate_Res": "blue", 'successRate_Sim': '#742802'})
