import argparse
from . import PDFToTextConverter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="visionpdftext",
        description='Convert PDF to text using OpenAI API'
    )
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
    for page_num, text in converter.process():
        print(f"Page {page_num} Text:\n{text}\n")
