# -*- coding: utf-8 -*-


# %% {"tags": ["remove_cell"]}
!jupyter nbconvert --to markdown "07-27-2019_const_labor.ipynb" --output="07-27-2019_const_labor.md" \
--TagRemovePreprocessor.enabled=True \
--TagRemovePreprocessor.remove_cell_tags="['remove_cell']" \
--TagRemovePreprocessor.remove_input_tags="['remove_input']" \
--TagRemovePreprocessor.remove_all_outputs_tags="['remove_output']" \
--TemplateExporter.exclude_input=False

# %% {"tags": ["remove_cell"]}
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
%matplotlib inline

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('sheets-fdaa4ad65b18.json', scope)

gc = gspread.authorize(credentials)


# %% {"tags": ["remove_cell"]}
%load_ext magic_markdown


# %% {"tags": ["remove_cell"]}
def pandas_df_to_markdown_table(df):
    from IPython.display import Markdown, display
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.to_csv(sep="|", index=False)))


# %% {"tags": ["remove_cell"]}
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1kUmVAuv8ZBjqHzzsGz353t-bshJ3vOGHfC_GXp6U7xg/edit?usp=sharing')

# Open sheet and read data.
worksheet = sh.worksheet("Quadro")

df = get_as_dataframe(worksheet, parse_dates=True, usecols=[0,1,2,3,4,5,6], skiprows=7, header=0)
df.head()


# %% {"tags": ["remove_cell"]}
# Convert to a pandas dataframe:
stat = pd.DataFrame(df[0:33])
stat = stat.apply(pd.to_numeric, errors='ignore')

stat = stat.drop([5,16], axis=0) #removes rows (5 and 16) with no information
stat.head()

# %% {"tags": ["remove_cell"]}
base = stat.loc[0:,["Anos",'base-Total','base-Homens', "base-Mulheres"]]
ganho = stat.loc[0:,["Anos",'Total','Homens', "Mulheres"]]

# %% {"tags": ["remove_input"]}
f, ax = plt.subplots(figsize=(12, 4.5))

ax=sns.lineplot(x="Anos", y="base-Homens",data=base, label="Homens",linewidth=3, alpha=0.6)
ax=sns.lineplot(x="Anos", y="base-Mulheres",data=base, label="Mulheres", linewidth=3)
ax=sns.lineplot(x="Anos", y="base-Total",data=base, label="Média", linewidth=1,linestyle=":")


sns.despine(f,offset=0, trim=False)

plt.grid(color="0.95", linestyle='-', linewidth=1)
plt.ylabel("Renumeração base (euros)")
plt.xlabel("Ano")
plt.title("Renumeração base média para Homens e Mulheres", fontsize=14);


# %% {"tags": ["remove_input"]}
f, ax = plt.subplots(figsize=(12, 4.5))

ax=sns.lineplot(x="Anos", y="Homens",data=ganho, label="Homens",linewidth=3,alpha=0.6)
ax=sns.lineplot(x="Anos", y="Mulheres",data=ganho, label="Mulheres", linewidth=3)
ax=sns.lineplot(x="Anos", y="Total",data=ganho, label="Média", linewidth=1,linestyle=":")

sns.despine(f,offset=0, trim=False)

plt.grid(color="0.95", linestyle='-', linewidth=1)
plt.ylabel("Ganho Médio (euros)")
plt.xlabel("Ano")
plt.title("Ganho Médio Mensal para Homens e Mulhers", fontsize=14);


# %% {"tags": ["remove_cell"]}
ganho_1985=141.6
ganho_2010=948.2

aumento=round((ganho_2010/ganho_1985)*100,1)
aumento_medio=round(aumento/25,2)

# %% {"tags": ["remove_input"]}
%%mmd

$\frac{141.6}{948.2} \times 100 = {{aumento}}$ %

$\frac{669.6}{25}={{aumento_medio}}$ %


# %% {"tags": ["remove_input"]}
a=ganho.sort_values(by='Anos', ascending=False).head(8)

b=(a
 .style
 .hide_index()
 .highlight_max(color='lightgreen', subset=['Homens', "Mulheres"])
 .highlight_min(color='#cd4f39', subset=['Homens', "Mulheres"])
 .set_caption('2010-2017 Ganho Médio Mensal para Homens e Mulhers'))

pandas_df_to_markdown_table(a)


# %% {"tags": ["remove_input"]}
pandas_df_to_markdown_table(stat)


