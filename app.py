import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import matplotlib.pyplot as plt

# Dictionnaire des mois en français
MOIS_FR = {
    'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
    'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
    'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
}

def parse_french_date(date_str):
    """
    Parse une date au format français (ex: "10 février 2024")
    """
    try:
        # Nettoyage de la chaîne
        date_str = date_str.strip().lower()
        
        # Extraction des composants de la date
        jour, mois, annee = date_str.split()
        
        # Conversion du jour et de l'année en nombres
        jour = int(jour)
        annee = int(annee)
        
        # Conversion du mois en nombre
        if mois in MOIS_FR:
            mois = MOIS_FR[mois]
        else:
            raise ValueError(f"Mois non reconnu: {mois}")
            
        # Création de la date
        return pd.Timestamp(year=annee, month=mois, day=jour)
    except Exception as e:
        st.error(f"Erreur lors du parsing de la date '{date_str}': {str(e)}")
        return None

# Fonction pour charger les données
@st.cache_data
def load_data():
    try:
        # Remplacer 'votre_fichier.csv' par le nom de votre fichier
        df = pd.read_csv('/mount/src/Web-analytics/avis_avec_risques.csv')
        
        # Conversion des dates avec gestion des erreurs
        df['date_experience'] = df['date_experience'].apply(parse_french_date)
        
        # Suppression des lignes avec des dates invalides
        invalid_dates = df['date_experience'].isna()
        if invalid_dates.any():
            st.warning(f"Attention: {invalid_dates.sum()} dates n'ont pas pu être analysées et seront ignorées.")
            df = df.dropna(subset=['date_experience'])
            
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {str(e)}")
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d'erreur

# Chargement des données
df = load_data()
# Titre principal
# Utilisation de markdown pour personnaliser le titre
st.markdown("<h2 style='text-align: center;'>📊 Identification des Problèmes Récurrents dans les Avis Clients Négatifs</h3>", unsafe_allow_html=True)
st.write("")
st.write("")
# Sidebar pour les filtres
st.sidebar.header("Filtres")
selected_brands = st.sidebar.multiselect(
    "Sélectionner les marques",
    options=df['brand'].unique(),
    default=df['brand'].unique()
)

# Filtrer les données selon la sélection
filtered_df = df[df['brand'].isin(selected_brands)]
# Mapping des ratings vers les labels de satisfaction avec emojis
satisfaction_labels = {
    1: "😠 Très insatisfait",
    2: "☹️ Insatisfait",
    3: "😐 Neutre",
}

# Ajouter une colonne "satisfaction_label" au DataFrame
filtered_df["satisfaction_label"] = filtered_df["rating"].map(satisfaction_labels)

# Layout en colonnes
col1, col2 = st.columns(2)

# Statistiques générales
with col1:
    st.subheader("Statistiques Générales")
    for brand in selected_brands:
        brand_df = filtered_df[filtered_df['brand'] == brand]
        
        # Créer un expander pour chaque marque
        with st.expander(f"🛒 {brand}"):
            st.write(f"Nombre total d'avis négatifs: {len(brand_df)}")
            
            
            # Note moyenne
            avg_rating = brand_df['rating'].mean()
            st.write(f"Note moyenne: {avg_rating:.2f}/5")

# Distribution des notes
with col2:
    # Définir les couleurs pour chaque marque
    color_map = {
    "Shein": "black",      # Shein en noir
    "Amazon": "#FF7F50",    # Amazon en orange
    "Temu": "#FFA500"      # Temu dans une nuance d'orange (ici, orange standard)
}

    # Créer l'histogramme avec les couleurs personnalisées
    fig_ratings = px.histogram(
        filtered_df,
        x="satisfaction_label",
        color="brand",
        barmode="group",
        histnorm="percent",
        title="Distribution des Notes (%)",
        color_discrete_map= color_map , # Appliquer le mapping des couleurs
        labels={
        "satisfaction_label": "Niveaux de Satisfaction",
        "percent": "Pourcentage"
    }
)

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig_ratings, use_container_width=True)

# Analyse des problèmes
st.subheader("Analyse des Problèmes")
col3, col4 = st.columns(2)

# Ajout d'un dictionnaire pour associer des emojis aux problèmes
problem_emojis = {
    "Problème de livraison" : "Livraison 🚚",
    "Problème de qualité du produit" : "Qualité du Produit❌",
    "Problème de remboursement" : "Remboursement 💸",
    "Problème de service client" : "Service Client📞",
    "Problème de taille ou couleur" : "taille/couleur 📏"
}

# Ajouter une colonne avec les emojis correspondants
filtered_df['problem'] = filtered_df['Identified Risk'].map(problem_emojis) 

# Définir les couleurs pour chaque marque
color_map = {
    "Shein": "black",      # Shein en noir
    "Amazon": "#FF7F50",    # Amazon en orange
    "Temu": "#FFA500"      # Temu dans une nuance d'orange (ici, orange standard)
}

    # Créer l'histogramme avec les couleurs personnalisées
fig_ratings = px.histogram(
        filtered_df,
        x="problem",
        color="brand",
        barmode="group",
        histnorm="percent",
        title="Distribution des Problèmes 📊 (%)",
        color_discrete_map= color_map , # Appliquer le mapping des couleurs
        labels={
        "problem": "problème",
        "percent": "Pourcentage"
    }
)

    # Afficher le graphique dans Streamlit
st.plotly_chart(fig_ratings, use_container_width=True)

# Téléchargement des données
st.sidebar.markdown("---")
st.sidebar.subheader("Télécharger les Données")
csv = filtered_df.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Télécharger les données filtrées (CSV)",
    data=csv,
    file_name="avis_clients_analyse.csv",
    mime="text/csv"
)
