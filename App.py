import streamlit as st

import os

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import imageio as iio

import PIL.Image

hide_st_style = """
                <style>
                header {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html = True)

def to_markdown(text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

st.title("Math Formulae Extractor")
st.write("---")

Image = st.file_uploader("Upload your Image!!")

'''
st.subheader("Or you can use Test Images!!!")
ImgList = os.listdir("TestImages")
ImgPath = st.selectbox("Images", ImgList)
if ImgPath and st.checkbox("Use Example Images", value = False):
        ImgPath = "TestImages/" + ImgPath
        Image = iio.imread(ImgPath)
'''
if Image:
        st.image(Image)

def APIConfig():
        genai.configure(api_key='AIzaSyBE1HLZuDQHbVz1C6MPD9FcvPbkeJqGrQU')
        model = genai.GenerativeModel('gemini-pro-vision')
        return model

model = APIConfig()

def Extractor(img):
        response = model.generate_content(["Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text.", img], stream=True)
        response.resolve()

        st.write(to_markdown(response.text))

        btn = st.download_button(label = "Download File", data = response.text, file_name = "Files/New.tex")

if Image and st.button("Extract"):
        img = PIL.Image.open(Image)

        with st.spinner("We'r Almost there!!!"):
                Extractor(img)
