from transformers import pipeline
import pandas as pd
# Définir le modèle zero-shot classification
classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")

# Définir les catégories de risque
candidate_labels = [
    "Problème de livraison",
    "Problème de qualité du produit",
    "Problème de remboursement",
    "Problème de service client",
    "Problème de taille ou couleur"
]

# Fonction pour classifier chaque avis et identifier le risque dominant
def identifier_risque(avis):
    if isinstance(avis, str):  # Vérifier que l'avis est bien une chaîne de caractères
        output = classifier(avis, candidate_labels, multi_label=False)
        return output["labels"][0]  # Prendre la catégorie avec la plus haute probabilité
    return "Inconnu"
#lire les données
df =  pd.read_csv("reviews.csv")
# Appliquer la classification à chaque avis
df["Identified Risk"] = df["review"].apply(identifier_risque)

# Sauvegarder le fichier avec la nouvelle colonne
df.to_csv("avis_avec_risques.csv", index=False)

print("Analyse terminée ! Fichier 'avis_avec_risques.csv' généré.")
