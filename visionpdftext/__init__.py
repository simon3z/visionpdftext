from pdf2image import convert_from_path
from openai import OpenAI
import os
import base64
from io import BytesIO

# Private global variable containing the prompt for the OpenAI model.
# The prompt requests a markdown description suitable for RAG systems
# and instructs the model to output only the page content without any
# additional commentary or questions.
_PROMPT = (
    "Please extract the text from this image and provide a description in markdown "
    "format suitable for use with Retrieval-Augmented Generation (RAG) systems. "
    "Output only the content of the page, without any additional information, "
    "questions, or commentary."
)

class PDFToTextConverter:
    def __init__(self, pdf_path, api_key=None, base_url=None, model=None):
        self.pdf_path = pdf_path
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL') or None
        self.model = model or os.getenv('OPENAI_MODEL') or "gpt-4o-mini"
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable or pass it as a parameter.")

    def process(self):
        """Generator that yields each page number and extracted text."""
        # Convert PDF to images
        images = convert_from_path(self.pdf_path)
        print(f"Extracted {len(images)} pages from PDF.")
        
        # Prepare OpenAI client once
        client_args = {}
        if self.api_key:
            client_args['api_key'] = self.api_key
        if self.base_url:
            client_args['base_url'] = self.base_url
        client = OpenAI(**client_args)

        # Process each image and yield text
        for idx, image in enumerate(images, start=1):
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            b64_image = base64.b64encode(image_bytes).decode("utf-8")
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": _PROMPT},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                    ]}
                ]
            )
            text = response.choices[0].message.content
            yield idx, text
