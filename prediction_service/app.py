import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import tensorflow as tf
"""
# Deep Classifier Project
### First classifier

"""
##Load model
model= tf.keras.models.load_model("model.h5")
uploaded_file= st.file_uploader("Choose the picture")
if uploaded_file is not None:
    image= Image.open(uploaded_file)
    img= np.array(image)
    img_resize= tf.image.resize(img,[224,224])
    img_reshape= np.expand_dims(img_resize,axis=0)
    output= model.predict(img_reshape).argmax(axis=1)
    if output==0:
        Result= "Cat"
    else:
        Result="Dog"
    st.image(image, caption=f"Its a {Result}")