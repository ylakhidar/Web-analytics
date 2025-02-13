# Analyse des Avis Clients sur les Plateformes de E-commerce

## Description du Projet

Ce projet vise à collecter, analyser et visualiser les avis négatifs des clients sur différentes plateformes e-commerce (`Amazon`, `Temu`, `Shein`). Grâce au **web scraping**, aux modèles  **Zero-Shot Learning** basé sur modèles pré-entrainés (Bert, Bart etc.) et à une application **Streamlit**, il permet d'identifier les problèmes les plus fréquents liés aux commandes en ligne et d'anticiper les risques potentiels.

---
## Architecture du Projet
📂 Web-analytics
│── 📝 README.md              # Documentation du projet
│── 📝 requirements.txt       # Dépendances Python nécessaires
│── 📝 web_scraping.py        # Script de collecte et stockage des avis
│── 📝 analyse_avis.py       # Analyse des avis avec un modèle IA
│── 📝 app.py                # Application Streamlit de visualisation
│── 📝 reviews.csv           # Avis collectés       
│── 📝 avis_avec_analyse.csv # Avis analysés avec problèmes identifiés par l'IA 

---

##  Fonctionnalités Principales

1. **Web Scraping des Avis Clients**  
   - Extraction des avis depuis [Trustpilot](https://fr.trustpilot.com/) pour `Amazon`, `Temu` et `Shein`  
   - Filtrage des avis avec une note **inférieure à 3**  
   - Stockage des données dans un fichier `reviews.csv`

2. **Analyse des Avis avec IA (Zero-Shot Learning)**  
   - Utilisation d'un modèle **Transformers** pour identifier les problèmes liés aux avis négatifs  
   - Classification des problèmes en catégories : `Livraison`, `Service Client`, `Remboursement`, etc.  
   - Stockage des données enrichies dans `avis_avec_analyse.csv`

3. **Application de Visualisation (Streamlit)**  
   - Interface interactive permettant d'explorer les avis négatifs  
   - Graphiques pour visualiser les tendances des problèmes par marque  
   - Indicateurs du niveau de satisfaction client  
