"""
app.py
------
The Streamlit web application.

Run it with:

    streamlit run app.py

What the user sees:
  - a box to upload a fish photo
  - the photo they uploaded
  - the predicted species, in big letters
  - how confident the model is, for every species
"""

import json
import os

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from tensorflow.keras.models import load_model

from src import config

# ----------------------------------------------------------------------
# PAGE SETTINGS - must be the first Streamlit command in the file
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Fish Species Classifier",
    page_icon="🐟",
    layout="centered",
)

# Where the trained model and the class names were saved by train_all_models.py
MODEL_PATH = os.path.join(config.MODELS_DIR, "best_model.h5")
CLASS_NAMES_PATH = os.path.join(config.MODELS_DIR, "class_names.json")
BEST_NAME_PATH = os.path.join(config.MODELS_DIR, "best_model_name.txt")


# ----------------------------------------------------------------------
# LOADING THE MODEL
# ----------------------------------------------------------------------
# @st.cache_resource tells Streamlit: "run this function once, then keep
# the result in memory". Without it, the model would reload from disk
# every single time the user clicks something, which is very slow.
@st.cache_resource
def load_trained_model():
    """Load the best saved model and the list of species names."""

    # If training has not been run yet, there is nothing to load.
    if not os.path.exists(MODEL_PATH):
        return None, None, None

    model = load_model(MODEL_PATH)

    with open(CLASS_NAMES_PATH) as f:
        class_names = json.load(f)

    # Which architecture won? (just for display)
    best_name = "Unknown"
    if os.path.exists(BEST_NAME_PATH):
        with open(BEST_NAME_PATH) as f:
            best_name = f.read().strip()

    return model, class_names, best_name


def prepare_image(uploaded_image):
    """
    Turn the uploaded picture into the exact shape the model expects.

    The model was trained on 224x224 RGB images with pixel values
    between 0.0 and 1.0, so the uploaded image must match that exactly.
    """

    # 1. make sure it is RGB (a PNG can have a 4th transparency channel)
    image = uploaded_image.convert("RGB")

    # 2. resize to 224 x 224
    image = image.resize(config.IMAGE_SIZE)

    # 3. turn the picture into numbers
    image_array = np.array(image)

    # 4. divide by 255, exactly like ImageDataGenerator(rescale=1./255) did
    image_array = image_array / 255.0

    # 5. the model expects a BATCH of images, not one image.
    #    np.expand_dims turns shape (224, 224, 3) into (1, 224, 224, 3),
    #    which means "a batch containing one image".
    image_batch = np.expand_dims(image_array, axis=0)

    return image_batch


# ----------------------------------------------------------------------
# THE PAGE ITSELF
# ----------------------------------------------------------------------

st.title("🐟 Fish Species Classifier")
st.write(
    "Upload a photo of a fish and the model will predict its species "
    "and show how confident it is."
)

model, class_names, best_name = load_trained_model()

# If there is no trained model yet, explain what to do and stop here.
if model is None:
    st.error(
        "No trained model found.\n\n"
        "Run `python train_all_models.py` first - it saves "
        "`models/best_model.h5`, which this app needs."
    )
    st.stop()

# A small information box in the sidebar
with st.sidebar:
    st.header("About")
    st.write(f"**Model in use:** {best_name}")
    st.write(f"**Species it knows:** {len(class_names)}")
    st.write("**Input size:** 224 x 224 pixels")
    st.divider()
    st.write("**Species list**")
    for name in class_names:
        st.write(f"- {name}")

# The upload box
uploaded_file = st.file_uploader(
    "Choose a fish image", type=["jpg", "jpeg", "jfif", "png", "webp", "bmp"]
)

if uploaded_file is not None:

    # Open the uploaded file as a picture
    image = Image.open(uploaded_file)

    # Show it to the user
    st.image(image, caption="Your image", use_container_width=True)

    # st.spinner shows a "please wait" message while the code inside runs
    with st.spinner("Thinking ..."):
        image_batch = prepare_image(image)

        # predict() gives one row of probabilities. [0] takes that row.
        probabilities = model.predict(image_batch)[0]

    # The position of the biggest probability is the predicted class
    best_position = int(np.argmax(probabilities))
    predicted_species = class_names[best_position]
    confidence = float(probabilities[best_position]) * 100

    # ------------------------------------------------------------------
    # SHOW THE ANSWER
    # ------------------------------------------------------------------
    st.success(f"### Prediction: {predicted_species}")
    st.metric("Confidence", f"{confidence:.2f}%")

    # ------------------------------------------------------------------
    # SHOW THE CONFIDENCE FOR EVERY SPECIES
    # ------------------------------------------------------------------
    st.subheader("Confidence for every species")

    # Build a small table: species name + its probability as a percentage
    scores_table = pd.DataFrame(
        {
            "Species": class_names,
            "Confidence (%)": (probabilities * 100).round(2),
        }
    )

    # Sort it so the most likely species is at the top
    scores_table = scores_table.sort_values("Confidence (%)", ascending=False)

    # A bar chart...
    st.bar_chart(scores_table.set_index("Species"))

    # ...and the numbers underneath
    st.dataframe(scores_table, hide_index=True, use_container_width=True)

else:
    st.info("Waiting for an image. Drag a fish photo into the box above.")
