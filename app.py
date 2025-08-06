import streamlit as st
import pandas as pd 
import os
from recommender import recommender_functions as rf

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'data_reduced.csv')
data = pd.read_csv(DATA_PATH)



st.set_page_config(
    page_title="PlentyofCats",
    page_icon=":cat:",
    layout="centered"
)

st.title('Plenty of Cats:cat::smile_cat::smiley_cat::heart_eyes_cat::smirk_cat::kissing_cat:')
st.header("Welcome!")
st.write("This is a recommender engine for cat owners looking to adopt another cat.")
st.subheader("How to Use:")

st.markdown("1. Select the sex of the cats you wish to see")
st.markdown("2. Rate your cat across four personality traits")
st.markdown("3. By default you will get recommendations that are the most similar in each trait. If you'd like to see cats that are opposite for a specific trait, check the checkbox")
st.markdown("4. You can also see recommendations based on only specific traits using the dropdown")


st.markdown('#### I want to see:')
status = st.radio("I want to see:", ["Female cats only", "Male cats only", "Both"], label_visibility='collapsed', index=2)
if status == "Female cats only":
    sex_filter = 0
elif status == "Male cats only":
    sex_filter = 1
else:
    sex_filter = 'all'
    
st.text("Rate your cat's personality traits:")

all_traits = ['Anxiety', 'Social Dominance', 'Activity Level', 'Social Reactivity']
trait_mappings = {
    'Anxiety': 'Factor1',
    'Social Dominance': 'Factor2',
    'Activity Level': 'Factor3',
    'Social Reactivity': 'Factor4'
}

st.markdown("### Anxiety/Confidence")
factor1 = st.slider("Factor1", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("How nervous your cat is. A higher score means that you cat is shy, fearful, and insecure; likely to hide and avoid strangers. A lower score means that they are confident and trusting; unbothered by new people or environments.")

st.markdown('### Social Dominance')
factor2 = st.slider("Factor2", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("How assertive your cat is in social situations. A higher score means that they are more bold, territorial, or even aggressive to other cats. A lower score means they are easygoing and likely get along well with other cats.")

st.markdown('### Activity level')
factor3 = st.slider("Factor3", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("A higher score means a curious, active, and playful cat. A lower score means a calmer, passive cat")

st.markdown('### Social Reactivity')
factor4 = st.slider("Factor4", min_value=1, max_value=7, label_visibility='collapsed')

user = [factor1, factor2, factor3, factor4]

st.markdown("#### Number of recommendations:")
number = st.number_input("How many cats:", value=10, step=1, key='count', label_visibility='collapsed')

advanced = st.toggle("Advanced mode", key='advanced')

if advanced:
    
    selected_same = st.multiselect("Similar:", all_traits, key='ss')
    ss_mapped = [trait_mappings[trait] for trait in selected_same]
    selected_different = st.multiselect("Different:", all_traits, key='sd')
    sd_mapped = [trait_mappings[trait] for trait in selected_different]
    selected_factors = ss_mapped + sd_mapped

    overlap = set(selected_same).intersection(selected_different)
    empty = not selected_same and not selected_different

    if overlap:
        st.warning(f"Traits {list(overlap)} cannot be in both similarity and diversity selections. Please fix.")
    
    advanced_start = st.button("See cats! :smile_cat:", disabled=bool(overlap or empty), key='as')

    if advanced_start and not overlap:
        advanced_results = rf.recommend(
            user,
            data,
            same_traits=ss_mapped,
            different_traits=sd_mapped,
            n_recs=number,
            factors=selected_factors,
            sex=sex_filter)
        
        st.subheader("Here are your top matches! 😻")
        st.dataframe(advanced_results)
else: 

    start = st.button("See cats! :smile_cat:")

    same_traits = []
    different_traits = []

    if start:
        results = rf.recommend(
        user,
        data,
        n_recs=number,
        sex=sex_filter
    )

        st.subheader("Here are your top matches! 😻")
        st.dataframe(results)
    











