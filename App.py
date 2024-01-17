import streamlit as st

import os

import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

from openai import OpenAI
import openai

import PIL.Image
import base64
import io

from transformers import TrOCRProcessor
from transformers import VisionEncoderDecoderModel

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

Prompt = "From this Given Image, please extract Mathematical formulae one by one (Don't extract any textual matter) and convert them into LaTeX code (you should not generate any extra content other than formulae). If no Math formula found in the image just return ==> No Math Formula found in the Image!!. Remember just generate the Math Formulae in LaTeX code, dont even include title tag for ur reponse!!"
	
def ChatGPT(Image):
	#"Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text. Remember dont include any text other than formulae and put each formula line by line if it has multiple formulae."
	buffer = io.BytesIO(Image.read())
	base64_encoded_image = base64.b64encode(buffer.read()).decode("utf-8")
	data = f"data:image/jpeg;base64,{base64_encoded_image}"
	APIKey = st.text_input("Enter your GPT-4 API Key")
	if APIKey:
		try:
			client = OpenAI(api_key = APIKey)
			if st.button("Extract"):
				with st.spinner("We'r Almost there!!!"):
					response = client.chat.completions.create(
						model="gpt-4-vision-preview",
						messages=[
						  {
						    "role": "user",
						    "content": [
						      {"type": "text", "text": Prompt},
						      {
							"type": "image_url",
							"image_url": {
							"url": data,
							},
						      },
						    ],
						  }
						],
						max_tokens=1000,
					      )
					k = response.choices[0].message.content
					if k != "No Math Formula found in the Image!!":
						st.code(response.choices[0].message.content)
						btn = st.download_button(label = "Download File", data = response.choices[0].message.content, file_name = "MathPixie.tex")
					else:
						st.error("Upload an Image with atleast one Math Formula!!")
		except openai.AuthenticationError:
			st.error("Please enter Authorized API Key!!")

def GeminiAI(Image):
	#"Hey Gemini, Extract Mathematical formulae from this Image and convert that into LaTeX Text."
	genai.configure(api_key='AIzaSyB8ayw3zz3HuZDPYJuyS4rYUcnj8cH28XI')
	model = genai.GenerativeModel('gemini-pro-vision')
	image = PIL.Image.open(Image)
	if st.button("Extract"):
		with st.spinner("We'r Almost there!!!"):
			response = model.generate_content([Prompt, image], stream=True)
			response.resolve()
			k = to_markdown(response.text)
			if k != ">  No Math Formula found in the Image!!":
				st.code(to_markdown(response.text))
				btn = st.download_button(label = "Download File", data = response.text, file_name = "MathPixie.tex")
			else:
				st.error("Upload an Image with atleast one Math Formula!!")

def Sesame(Image, processor, model):
	if st.button("Extract"):
		with st.spinner("We'r Almost there!!!"):
			image = PIL.Image.open(Image).convert("RGB")
			pixel_values = processor(images=image, return_tensors="pt").pixel_values
		
			generated_ids = model.generate(pixel_values)
			generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
			
			st.code(generated_text)

def main():
	st.title("Math Formulae Extractor")
	st.write("Leverage the Power of Gemini, GPT-4 and extract Maths Formulae from Images....")
	st.write("---")

	with st.spinner("Loading the Model"):
		processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
		model = VisionEncoderDecoderModel.from_pretrained("CodeKapital/SESAME")

	ModelName = st.selectbox("Select a Model", ("gemini-pro-vision", "gpt-4-vision-preview", "Sesame"))
	
	Image = st.file_uploader("Upload your Image!!")
	if Image:
		st.image(Image)
		
	if ModelName == "gpt-4-vision-preview" and Image:
		ChatGPT(Image)
	elif ModelName == "gemini-pro-vision" and Image:
		GeminiAI(Image)
	elif ModelName == "Sesame" and Image:
		Sesame(Image, processor, model)
if __name__ == "__main__":
    main()
