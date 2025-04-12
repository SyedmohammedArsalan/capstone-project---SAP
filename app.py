import streamlit as st
from detect import detect_clothes
from recommend import get_style_recommendation

st.title("AI Fashion Style Recommender")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])

if uploaded_file:
    with open("input.jpg", "wb") as f:
        f.write(uploaded_file.read())
    st.image("input.jpg", caption="Uploaded Image", use_column_width=True)

    st.write("Detecting clothes...")
    items = detect_clothes("input.jpg")

    if items:
        st.write("Cropped clothing items:")
        for img in items:
            st.image(img, width=150)

        st.write("Generating style feedback...")
        desc = ", ".join([f"item {i+1}" for i in range(len(items))])
        feedback = get_style_recommendation(desc)

        st.subheader("Style Suggestions")
        st.write(feedback)
