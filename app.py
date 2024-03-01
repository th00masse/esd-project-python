import streamlit as st
from fixtures import df, club_names
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
import requests

st.title('Application Thomasse Data Football')
st.markdown('Une application qui scrappe les données du championnat anglais en temps réels et qui donne une prédiction pour sur le résultat du match')

logo_path = "logo.png"
logo = Image.open(logo_path)

st.image(logo, width=100)  # Ajuster la largeur selon vos besoins

url = "https://fbref.com/en/comps/9/Premier-League-Stats"

st.write("## Dataset - Classement de la Premier League")
st.write(pd.read_html(url)[0])  # Supposons que la première table soit celle qui vous intéresse

st.write("## Top Team Scorer de la Premier League")
df = pd.read_html(url)[0]

fig, ax = plt.subplots()
ax.bar(df['Squad'], df['Top Team Scorer'], color='green')
ax.set_xlabel('Équipes')
ax.set_ylabel('Top Team Scorer')
ax.set_title('Top Team Scorer de la Premier League')

plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

df_sorted_by_goals = df.sort_values(by='GF', ascending=False)

fig, ax = plt.subplots()
ax.plot(df_sorted_by_goals['Squad'], df_sorted_by_goals['GF'], marker='o', color='purple', linestyle='-')
ax.set_xlabel('Équipes')
ax.set_ylabel('Nombre de buts marqués')
ax.set_title('Classement des équipes par nombre de buts marqués')

plt.xticks(rotation=45, ha='right')

st.pyplot(fig)

df.fillna(value={'Playing Time': 0, 'Performance': 0, 'Expected': 0, 'Progression': 0, 'Per 90 Minutes': 0}, inplace=True)

st.sidebar.title("Sélection des équipes")

equipe1 = st.sidebar.selectbox('Équipe 1', df['Squad'])
equipe2 = st.sidebar.selectbox('Équipe 2', df['Squad'])

st.write(f"Statistiques pour {equipe1} :")
st.write(df[df['Squad'] == equipe1])

st.write(f"Statistiques pour {equipe2} :")
st.write(df[df['Squad'] == equipe2])

if st.sidebar.button('Calculer la probabilité de victoire'):
    # Simulation de probabilités aléatoires (à remplacer par votre logique de prédiction)
    proba_equipe1 = np.random.uniform(0, 1)
    proba_equipe2 = np.random.uniform(0, 1)

    st.sidebar.write(f"Probabilité de victoire pour {equipe1}: {proba_equipe1:.2%}")
    st.sidebar.write(f"Probabilité de victoire pour {equipe2}: {proba_equipe2:.2%}")

    if proba_equipe1 > proba_equipe2:
        st.sidebar.write(f"L'équipe gagnante est {equipe1}")
        top_scorer_equipe1 = df.loc[df['Squad'] == equipe1, 'Top Team Scorer'].values[0]
        st.sidebar.write(f"Meilleur buteur de {equipe1}: {top_scorer_equipe1}")
    elif proba_equipe1 < proba_equipe2:
        st.sidebar.write(f"L'équipe gagnante est {equipe2}")
        top_scorer_equipe2 = df.loc[df['Squad'] == equipe2, 'Top Team Scorer'].values[0]
        st.sidebar.write(f"Meilleur buteur de {equipe2}: {top_scorer_equipe2}")
    else:
        st.sidebar.write("Match nul")
