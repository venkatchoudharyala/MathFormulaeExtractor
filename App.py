import streamlit as st

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import PIL.Image

def to_markdown(text):
        text = text.replace('•', '  *')
        return textwrap.indent(text, '> ', predicate=lambda _: True)

st.title("Math Formulae Extractor")
st.write("---")

Image = st.file_uploader("Upload your Image!!")
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
