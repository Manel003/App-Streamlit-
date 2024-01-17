import streamlit as st
import sqlite3
import pandas as pd

# Fonction pour créer la table s'il n'existe pas
def creer_table():
    c.execute('''
          CREATE TABLE IF NOT EXISTS utilisateurs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              nom TEXT,
              prenom TEXT,
              email TEXT
          )
          ''')
    conn.commit()

# Fonction pour ajouter un utilisateur à la base de données
def ajouter_utilisateur(nom, prenom, email):
    c.execute('''
              INSERT OR IGNORE INTO utilisateurs (nom, prenom, email)
              VALUES (?, ?, ?)
              ''', (nom, prenom, email))
    conn.commit()

# Fonction pour récupérer tous les utilisateurs de la base de données
def recuperer_utilisateurs(recherche):
    query = f'SELECT id, nom, prenom, email FROM utilisateurs WHERE nom LIKE "%{recherche}%" OR prenom LIKE "%{recherche}%" OR email LIKE "%{recherche}%"'
    c.execute(query)
    return c.fetchall()

# Fonction pour supprimer un ou plusieurs utilisateurs de la base de données
def supprimer_utilisateurs(ids_utilisateurs):
    if ids_utilisateurs:
        placeholders = ', '.join(['?'] * len(ids_utilisateurs))
        c.execute(f'DELETE FROM utilisateurs WHERE id IN ({placeholders})', tuple(ids_utilisateurs))
        conn.commit()

# Connexion à la base de données SQLite
conn = sqlite3.connect('Z:/BUT3 SEM-5/Streamlit/data.db')
c = conn.cursor()

# Créer la table s'il n'existe pas
creer_table()

# Page principale de l'application
def main():
    st.title('Formulaire et Interface Utilisateurs')

    # Changer la couleur de fond
    st.markdown(
    """
    <style>
        body {s
            background-color: #CCEEFF;  /* Remplacez cette couleur par celle de votre choix */
        }
    </style>
    """,
    unsafe_allow_html=True
)


    # Créer un formulaire avec des champs pour nom, prénom et email
    nom = st.text_input('Nom')
    prenom = st.text_input('Prénom')
    email = st.text_input('Email')

    # Bouton pour enregistrer les informations dans la base de données
    if st.button('Enregistrer'):
        if nom and prenom and email:
            # Appeler la fonction pour ajouter l'utilisateur
            ajouter_utilisateur(nom, prenom, email)
            st.success('Utilisateur enregistré avec succès!')
        else:
            st.warning('Veuillez remplir tous les champs.')

    # Afficher ou cacher tous les utilisateurs de la base de données
    show_db = st.checkbox('Afficher la base de données')
    if show_db:
        st.subheader('Utilisateurs enregistrés')

        # Barre de recherche
        recherche = st.text_input('Rechercher dans la base de données')

        # Récupérer les utilisateurs en fonction de la recherche
        utilisateurs = recuperer_utilisateurs(recherche)

        if utilisateurs:
            # Convertir la liste de tuples en DataFrame
            df = pd.DataFrame(utilisateurs, columns=["ID", "Nom", "Prénom", "Email"])

            # Afficher le DataFrame
            st.dataframe(df)

            # Menu déroulant multiselect pour sélectionner les utilisateurs à supprimer
            utilisateurs_a_supprimer = st.multiselect('Sélectionner les utilisateurs à supprimer', df['ID'].tolist())

            # Bouton pour supprimer les utilisateurs sélectionnés
            if st.button('Supprimer'):
                supprimer_utilisateurs(utilisateurs_a_supprimer)
                st.success('Utilisateurs supprimés avec succès!')
        else:
            st.info('Aucun utilisateur enregistré.')

if __name__ == '__main__':
    main()








