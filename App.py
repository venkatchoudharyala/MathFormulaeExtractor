import streamlit as st

import os

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import imageio as iio

from openai import OpenAI

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
st.write("Leverage the Power of Gemini and extract Maths Formulae from Images....")
st.write("---")

ModelName = st.selectbox("Select a Model", ("GPT-4-vision-preview", "gemini-pro-vision"))

Image = st.file_uploader("Upload your Image!!")

if Image:
        st.image(Image)

def APIConfig(ModelName):
        if ModelName == "gemini-pro-vision":
                genai.configure(api_key='AIzaSyBE1HLZuDQHbVz1C6MPD9FcvPbkeJqGrQU')
                model = genai.GenerativeModel('gemini-pro-vision')
                return model
        elif ModelName == "GPT-4-vision-preview":
                APIKey = st.text_input("Enter your GPT-4 API Key")
                client = OpenAI(api_key = APIKey)
                return client

model = APIConfig(ModelName)

def Extractor(img, ModelName):
        if ModelName == "gemini-vision-pro":
                response = model.generate_content(["Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text.", img], stream=True)
                response.resolve()

                st.write(to_markdown(response.text))

                btn = st.download_button(label = "Download File", data = response.text, file_name = "Files/New.tex")
        elif ModelName == "GPT-4-vision-preview":
                response = client.chat.completions.create(
                                model="gpt-4-vision-preview",
                                messages=[
                                  {
                                    "role": "user",
                                    "content": [
                                      {"type": "text", "text": "Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text."},
                                      {
                                        "type": "image",
                                        "image":img
                                      },
                                    ],
                                  }
                                ],
                                max_tokens=300,
                              )
                st.write(response.choices[0])
if Image and st.button("Extract"):
        img = PIL.Image.open(Image)

        with st.spinner("We'r Almost there!!!"):
                Extractor(img, ModelName)
