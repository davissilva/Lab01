from typing import Type
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df = pd.read_csv('dadosRepositorios.csv')

#conversão do tempo desde a ultima atualização
df['hoursSinceUpdate'] = pd.to_timedelta(
    df['daysSinceUpdate']).dt.components['hours']

box_plotes = [
    'age', 'pullRequests', 'releases', 'issuesRatio', 'hoursSinceUpdate'
]

sns.set(rc={'figure.figsize': (8, 10)})

#Resposta RQ1, RQ2, RQ3, RQ4 e RQ6
for i in box_plotes:
    median = df[i].median()
    max_value = df[i].max()
    min_value = df[i].min()
    print('Mediana', i, ':', median)
    print('Maior', i, ':', max_value)
    print('Menor', i, ':', min_value)
    ax = sns.violinplot(data=df, y=i, width=0.6)
    sns.boxplot(data=df,
                y=i,
                width=0.1,
                color='white',
                boxprops={'zorder': 2},
                ax=ax)

    plt.show()

sns.set(rc={'figure.figsize': (10, 10)})

#Resposta RQ5
top_rated_languages = [
    'JavaScript', 'Python', 'Java', 'Typescript', 'C#', 'C++', 'PHP', 'Shell',
    'C', 'Ruby'
]

languages = df.query('primaryLanguage in @top_rated_languages').groupby(
    'primaryLanguage')['repository'].count().reset_index(
        name='count').sort_values('count', ascending=False)

plt.bar(languages['primaryLanguage'], languages['count'])
plt.xticks(rotation=90)
plt.xlabel('Linguagem')
plt.ylabel('Quantidade de Repositórios')

for i, v in enumerate(languages['count']):
    plt.text(i, v, str(v), ha='center', va='bottom', fontweight='bold')

plt.show()
