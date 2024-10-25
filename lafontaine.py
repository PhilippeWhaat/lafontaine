import pandas as pd
import random
import streamlit as st

# Charger le fichier CSV contenant les fables
fables_df = pd.read_csv('fables_with_verse_numbers.csv', index_col='Verse Number')

def generate_rhymed_fable(verse_count):
    max_verses = 40
    if verse_count > max_verses:
        st.warning(f"Le nombre de vers est limité à {max_verses}. Génération de {max_verses} vers.")
        verse_count = max_verses
    
    generated_fable = []
    verse_num = 1
    
    while verse_num <= verse_count:
        # Sélectionner de manière aléatoire une fable qui a un vers à ce numéro et qui n'est pas NaN
        available_fables = [fable for fable in fables_df.columns 
                            if verse_num in fables_df.index and pd.notna(fables_df.at[verse_num, fable])]

        if available_fables:
            chosen_fable = random.choice(available_fables)
            
            # Prendre deux vers successifs si possible pour respecter les rimes
            if verse_num < verse_count and verse_num + 1 in fables_df.index and pd.notna(fables_df.at[verse_num + 1, chosen_fable]):
                chosen_verse_1 = fables_df.at[verse_num, chosen_fable]
                chosen_verse_2 = fables_df.at[verse_num + 1, chosen_fable]
                generated_fable.append(str(chosen_verse_1))
                generated_fable.append(str(chosen_verse_2))
                verse_num += 2
            else:
                # Si on ne peut pas trouver une paire, on prend un seul vers
                if pd.notna(fables_df.at[verse_num, chosen_fable]):
                    chosen_verse = fables_df.at[verse_num, chosen_fable]
                    generated_fable.append(str(chosen_verse))
                verse_num += 1
        else:
            verse_num += 1
    
    # Retourner la fable générée
    return "\n".join(generated_fable)

# URL du logo
logo_url = "https://raw.githubusercontent.com/PhilippeWhaat/lafontaine/refs/heads/main/logo.png"

# Créer deux colonnes pour aligner le texte à gauche et le logo à droite
col1, col2 = st.columns([3, 1])  # Ajuster les proportions si nécessaire

with col1:
    st.title("Générateur de Fables Aléatoires de La Fontaine")
    st.write("Entrez le nombre de vers pour générer une fable aléatoire inspirée de La Fontaine.")

with col2:
    st.image(logo_url, width=150)

# Sélection de l'utilisateur pour le nombre de vers
verse_count = st.slider("Nombre de vers dans la fable", min_value=1, max_value=40, value=10)

# Bouton pour générer la fable
if st.button("Générer la fable"):
    random_fable = generate_rhymed_fable(verse_count)
    st.subheader("Votre fable générée :")
    st.text(random_fable)

# Ajouter des crédits en bas de la page avec un lien vers GitHub
st.markdown("---")
st.markdown(
    "✨ Créé par [PhilippeWhaat](https://github.com/PhilippeWhaat) | "
    "Inspiré par Piroteknik. Merci pour votre visite !"
)