# app.py
import os
import streamlit as st
from PIL import Image
from openai import OpenAI

st.set_page_config(page_title="Krishi-Sajag", page_icon="🌱")
st.title("Krishi-Sajag — AI Crop Advisor (Prototype)")

# Load API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("Set the OPENAI_API_KEY environment variable before running.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

st.markdown("Upload an image (optional) and/or type the crop symptom. Then click **Get Advice**.")

# Inputs
photo = st.file_uploader("Upload crop/leaf photo (optional)", type=["png", "jpg", "jpeg"])
if photo:
    img = Image.open(photo)
    st.image(img, caption="Uploaded image", use_column_width=True)

symptoms = st.text_area("Describe the problem (e.g., 'tomato leaves have black spots')", height=120)

if st.button("Get Advice"):
    if not symptoms and not photo:
        st.warning("Please provide a description or upload an image.")
    else:
        # Build a short prompt for the model
        prompt = (
            "You are an expert agricultural assistant for small farmers in India. "
            "A farmer reports the following (keep response simple & actionable):\n\n"
        )
        if symptoms:
            prompt += f"Farmer description: {symptoms}\n\n"
        if photo:
            prompt += "An image was uploaded by the farmer (image not analyzed in this prototype). "
            prompt += "Mention that an image was provided and advise next steps (e.g., request clearer photo or consult local expert if uncertain).\n\n"
        prompt += (
            "Now: give a concise diagnosis (if possible), 3 practical steps (preventive and treatment), "
            "one low-cost organic option, and a short safety note. End with a confidence level (low/medium/high)."
        )

        with st.spinner("Contacting the model..."):
            response = client.responses.create(
                model="gpt-4o",   # replace with a model you have access to (e.g., gpt-4o-mini)
                input=prompt,
                max_tokens=400,
            )

        # Display
        out = response.output_text if hasattr(response, "output_text") else response.output[0].content[0].text
        st.subheader("Recommendation")
        st.write(out)
