import streamlit as st
import pandas as pd
from func import  DiseasePredictor
def main():
    disease_predictor = DiseasePredictor()
    st.title("Disease Prediction using SVM Model and Classification: ")
    input_text = st.text_area("Enter the description of your symptoms",height=150)
    if st.button("Submit"):
        items = disease_predictor.predict(input_text)
        st.success("Possible Diseases:")
        st.table(items)

if __name__ == "__main__":
    main()
