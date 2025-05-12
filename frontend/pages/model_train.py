from turtle import onclick
import streamlit as st
from tensorflow.python.keras.models import load_model
import numpy as np
import tensorflow as tf

direc = st.text_input('Images directory')

st.title("Parameters")
eps = st.text_input('Epochs', key=1, placeholder='5')
estep = st.text_input('Steps per epoch', key=2, placeholder='100')
vstep = st.text_input('Validation steps', placeholder='50')

if st.button('Train the model'):
    if eps != "":
            if estep != "":
                if vstep!= "":
                    st.write('Fun!')
                else:
                    st.write('Fill the Validation steps field')
            else:
                st.write('Fill the Steps per epoch field')
    else:
        st.write('Fill the Epochs field')