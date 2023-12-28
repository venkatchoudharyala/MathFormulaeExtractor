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
import base64
import io

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
st.write("Leverage the Power of Gemini, GPT-4 and extract Maths Formulae from Images....")
st.write("---")

ModelName = st.selectbox("Select a Model", ("GPT-4-vision-preview", "gemini-pro-vision"))

Image = st.file_uploader("Upload your Image!!")

if Image:
        st.image(Image)

def API(ModelName):
        if ModelName == "gemini-vision-pro"
                genai.configure(api_key='AIzaSyBE1HLZuDQHbVz1C6MPD9FcvPbkeJqGrQU')
                model = genai.GenerativeModel('gemini-pro-vision')
                return model
        elif ModelName == "GPT-4-vision-preview"
                APIKey = st.text_input("Enter your GPT-4 API Key")
                client = OpenAI(api_key = APIKey)
                return client

model = API(ModelName)

def Extractor(img, ModelName):
        if ModelName == "gemini-vision-pro":
                response = model.generate_content(["Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text.", img], stream=True)
                response.resolve()

                st.write(to_markdown(response.text))

                btn = st.download_button(label = "Download File", data = response.text, file_name = "Files/New.tex")
        elif ModelName == "GPT-4-vision-preview":
                #url = "https://i.ytimg.com/vi/fk81g5c6PNQ/maxresdefault.jpg"
                response = model.chat.completions.create(
                                model="gpt-4-vision-preview",
                                messages=[
                                  {
                                    "role": "user",
                                    "content": [
                                      {"type": "text", "text": "Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text. Remember dont include any text other than formulae and put each formula line by line if it has multiple formulae."},
                                      {
                                        "type": "image_url",
                                        "image_url": {
                                        "url": img,
                                        },
                                      },
                                    ],
                                  }
                                ],
                                max_tokens=300,
                              )
                st.markdown(response.choices[0].message.content)
                btn = st.download_button(label = "Download File", data = response.choices[0].message.content, file_name = "Files/New.tex")
if Image and st.button("Extract"):
        if ModelName == "gemini-vision-pro":
                img = PIL.Image.open(Image)
                with st.spinner("We'r Almost there!!!"):
                        Extractor(img, ModelName)
        elif ModelName == "GPT-4-vision-preview":
                buffer = io.BytesIO(Image.read())
                base64_encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
                data = f"data:image/jpeg;base64,{base64_encoded_image}"
                with st.spinner("We'r Almost there!!!"):
                        Extractor(data, ModelName)

        
