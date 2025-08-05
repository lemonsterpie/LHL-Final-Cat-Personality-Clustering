import streamlit as st
import pandas as pd 
from recommender import model_functions as mf 

data = pd.read_csv('../data/data_reduced.csv')
factors = ['Factor1', 'Factor2', 'Factor3', 'Factor4']
means, stds, max_dists_sq = mf.compute_traits(data, factors)

st.set_page_config( #base information for our page
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
status = st.radio("I want to see:", ["Female cats only", "Male cats only", "Both"], label_visibility='collapsed')

st.text("Rate your cat's personality traits:")

st.markdown("### Anxiety/Confidence")
factor1 = st.slider("Factor1", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("How nervous your cat is. A higher score means that you cat is shy, fearful, and insecure; likely to hide and avoid strangers. A lower score means that they are confident and trusting; unbothered by new people or environments.")
check1 = st.checkbox("Find opposites", key='check1')

st.markdown('### Social Dominance')
factor2 = st.slider("Factor2", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("How assertive your cat is in social situations. A higher score means that they are more bold, territorial, or even aggressive to other cats. A lower score means they are easygoing and likely get along well with other cats.")
check2 = st.checkbox("Find opposites", key='check2')

st.markdown('### Activity level')
factor3 = st.slider("Factor3", min_value=1, max_value=7, label_visibility='collapsed')
st.markdown("A higher score means a curious, active, and playful cat. A lower score means a calmer, passive cat")
st.checkbox("Find opposites", key='check3')


st.markdown('### Social Reactivity')
factor4 = st.slider("Factor4", min_value=1, max_value=7, label_visibility='collapsed')
st.checkbox("Find opposites", key='check4')

st.multiselect("I want to pair ba sed on only these factors:", ['Factor1', 'Factor2', 'Factor3', 'Factor4'])

st.button("See cats! :smile_cat:")


