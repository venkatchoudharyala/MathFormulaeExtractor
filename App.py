import streamlit as st

import os

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

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
	
def ChatGPT(Image):
	buffer = io.BytesIO(Image.read())
	base64_encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
	data = f"data:image/jpeg;base64,{base64_encoded_image}"
	APIKey = st.text_input("Enter your GPT-4 API Key")
	if APIKey:
		client = OpenAI(api_key = APIKey)
		with st.spinner("We'r Almost there!!!"):
			response = client.chat.completions.create(
				model="gpt-4-vision-preview",
				messages=[
				  {
				    "role": "user",
				    "content": [
				      {"type": "text", "text": "Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text. Remember dont include any text other than formulae and put each formula line by line if it has multiple formulae."},
				      {
					"type": "image_url",
					"image_url": {
					"url": data,
					},
				      },
				    ],
				  }
				],
				max_tokens=300,
			      )
			st.markdown(response.choices[0].message.content)
			btn = st.download_button(label = "Download File", data = response.choices[0].message.content, file_name = "Files/New.tex")

def GeminiAI(Image):
	st.write("IN")
	genai.configure(api_key='AIzaSyBE1HLZuDQHbVz1C6MPD9FcvPbkeJqGrQU')
	model = genai.GenerativeModel('gemini-pro-vision')
	image = PIL.Image.open(Image)
	if st.button("Extract"):
		with st.spinner("We'r Almost there!!!"):
			response = model.generate_content(["Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text.", image], stream=True)
			response.resolve()
			st.write(to_markdown(response.text))
			btn = st.download_button(label = "Download File", data = response.text, file_name = "Files/New.tex")

def main():
	st.title("Math Formulae Extractor")
	st.write("Leverage the Power of Gemini, GPT-4 and extract Maths Formulae from Images....")
	st.write("---")
	
	ModelName = st.selectbox("Select a Model", ("gemini-pro-vision", "gpt-4-vision-preview"))
	
	Image = st.file_uploader("Upload your Image!!")
	if Image:
		st.image(Image)
		
	if ModelName == "gpt-4-vision-preview" and Image:
		ChatGPT(Image)
	elif ModelName == "gemini-vision-pro" and Image:
		GeminiAI(Image)
if __name__ == "__main__":
    main()
