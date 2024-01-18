import os

from transformers import VisionEncoderDecoderModel
from transformers import TrOCRProcessor

def CheckDir(Path):
	return os.path.exists(Path) and os.path.isdir(Path)

def createDir(Path):
	os.makedirs(Path, exist_ok=True)

def BootLoader():
	ProPath = "Processor/"
	ModelPath = "Sesame/"
	if not CheckDir(ProPath):
		createDir(ProPath)
		processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
		processor.save_pretrained(ProPath)
	if not CheckDir(ModelPath):
		counter = createDir(ModelPath)
		model = VisionEncoderDecoderModel.from_pretrained("CodeKapital/SESAME")
		model.save_pretrained(ModelPath)
		
		


