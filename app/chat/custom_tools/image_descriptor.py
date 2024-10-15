# This file is currently not integrated into the app

import os
import dotenv
import langchain
import base64  # Add this line

from langchain.chains import TransformChain
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain

# Set verbose
globals.set_debug(True)

dotenv.load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def load_image(inputs: dict) -> dict:
    """Load image from file and encode it as base64."""
    image_path = inputs["image_path"]
  
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    image_base64 = encode_image(image_path)
    return {"image": image_base64}


load_image_chain = TransformChain(
    input_variables=["image_path"],
    output_variables=["image"],
    transform=load_image
)

from langchain_core.pydantic_v1 import BaseModel, Field

class ImageInformation(BaseModel):
 """Information about an image."""
 outfit_description: str = Field(description="a short description of the outfit in the image (e.g. a red dress, a blue skirt, a green blouse, etc.)")
 outfit_pattern_type: str = Field(description="type of pattern on the outfit in the image(e.g. floral, striped, polka dots, etc.)")
 outfit_style: str = Field(description="the style of the outfit in the image (e.g. casual, formal, etc.)")


@chain
def image_model(inputs: dict) -> str | list[str] | dict:
 """Invoke model with image and prompt."""
 model = ChatOpenAI(temperature=0.5, model="gpt-4o", max_tokens=1024)
 msg = model.invoke(
             [HumanMessage(
             content=[
             {"type": "text", "text": inputs["prompt"]},
             {"type": "text", "text": parser.get_format_instructions()},
             {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{inputs['image']}"}},
             ])]
             )
 return msg.content


from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(pydantic_object=ImageInformation)
def get_image_information(image_path: str) -> dict:
   vision_prompt = """
   Given the image, provide the following information:
   - A description of the outfit in the image
   - The type of pattern on the outfit in the image
   - The style of the outfit in the image
   """
   vision_chain = load_image_chain | image_model | parser
   return vision_chain.invoke({'image_path': f'{image_path}', 
                               'prompt': vision_prompt})