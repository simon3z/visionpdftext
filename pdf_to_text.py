from pdf2image import convert_from_path
from openai import OpenAI
import os
import argparse
import base64

class PDFToTextConverter:
    def __init__(self, pdf_path, output_dir='images', api_key=None, base_url=None):
        self.pdf_path = pdf_path
        self.output_dir = output_dir
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = base_url or os.getenv('OPENAI_BASE_URL') or None
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Please set OPENAI_API_KEY environment variable or pass it as a parameter.")
        
    def convert_pdf_to_images(self):
        """Convert PDF to images and save them to output_dir"""
        images = convert_from_path(self.pdf_path)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        for i, image in enumerate(images):
            image.save(f"{self.output_dir}/page_{i+1}.png", "PNG")
        return f"Extracted {len(images)} pages to {self.output_dir}"

    def extract_text_from_image(self, image_path):
        """Extract text from an image using OpenAI API with optional custom base URL"""
        client_args = {}
        if self.api_key:
            client_args['api_key'] = self.api_key
        if self.base_url:
            client_args['base_url'] = self.base_url

        client = OpenAI(**client_args)
        prompt = "Extract text from this image:"
        with open(image_path, "rb") as image_file:
            b64_image = base64.b64encode(image_file.read()).decode("utf-8")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_image}"}}
                ]}
            ]
        )
        return response.choices[0].message.content

    def process(self):
        """Process the PDF: convert to images and extract text from each image"""
        # Convert PDF to images
        conversion_result = self.convert_pdf_to_images()
        print(conversion_result)
        
        # Extract text from each image
        text_pages = []
        if os.path.exists(self.output_dir) and os.listdir(self.output_dir):
            for filename in sorted(os.listdir(self.output_dir)):
                if filename.endswith('.png'):
                    image_path = os.path.join(self.output_dir, filename)
                    text = self.extract_text_from_image(image_path)
                    text_pages.append(text)
        else:
            print("No images found. Please check the PDF path and try again.")
            return None
            
        return text_pages

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert PDF to text using OpenAI API')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    parser.add_argument('--output_dir', type=str, default='images', help='Output directory for images')
    parser.add_argument('--api_key', type=str, help='OpenAI API key (can also be set via environment variable)')
    parser.add_argument('--base_url', type=str, help='Base URL for OpenAI API (optional)')

    args = parser.parse_args()

    converter = PDFToTextConverter(
        pdf_path=args.pdf_path,
        output_dir=args.output_dir,
        api_key=args.api_key,
        base_url=args.base_url
    )
    text_pages = converter.process()

    if text_pages:
        for i, text in enumerate(text_pages):
            print(f"Page {i+1} Text:\n{text}\n")
