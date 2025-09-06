from pdf2image import convert_from_path
from openai import OpenAI
import os
import argparse
import base64
from io import BytesIO

class PDFToTextConverter:
    def __init__(self, pdf_path, api_key=None, base_url=None, model=None):
        self.pdf_path = pdf_path
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL') or None
        self.model = model or os.getenv('OPENAI_MODEL') or "gpt-4o-mini"
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable or pass it as a parameter.")
        
    def convert_pdf_to_images(self):
        """Convert PDF to images and return them as a list."""
        images = convert_from_path(self.pdf_path)
        return images

    def extract_text_from_image(self, image_bytes):
        """Extract text from an image using OpenAI API with optional custom base URL."""
        client_args = {}
        if self.api_key:
            client_args['api_key'] = self.api_key
        if self.base_url:
            client_args['base_url'] = self.base_url

        client = OpenAI(**client_args)
        prompt = "Extract text from this image:"
        b64_image = base64.b64encode(image_bytes).decode("utf-8")
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                ]}
            ]
        )
        return response.choices[0].message.content

    def process(self):
        """Generator that yields each image's bytes so text can be extracted and printed immediately."""
        # Convert PDF to images
        images = self.convert_pdf_to_images()
        print(f"Extracted {len(images)} pages from PDF.")
        
        # Yield each image's bytes
        for idx, image in enumerate(images, start=1):
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            image_bytes = buffer.getvalue()
            yield idx, image_bytes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert PDF to text using OpenAI API')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('--api_key', type=str, help='OpenAI API key (can also be set via environment variable)')
    parser.add_argument('--base_url', type=str, help='Base URL for OpenAI API (optional)')
    parser.add_argument('--model', type=str, default=None, help='OpenAI model to use (default: gpt-4o-mini)')

    args = parser.parse_args()

    converter = PDFToTextConverter(
        pdf_path=args.pdf_path,
        api_key=args.api_key,
        base_url=args.base_url,
        model=args.model
    )

    # Iterate over the generator to extract and print text page by page
    for page_num, image_bytes in converter.process():
        text = converter.extract_text_from_image(image_bytes)
        print(f"Page {page_num} Text:\n{text}\n")
