# VisionPDFText

*This project was entirely coded using aider with local deepseek-r1 8B and gpt-oss 20B running on an NVIDIA RTX 4060TI with 8GB of memory. Inference is done with llama.cpp and llama-swap.*

**VisionPDFText** is a lightweight Python utility that converts PDF documents into text by leveraging the OpenAI vision API.  
Each page of the PDF is rendered as an image, sent to the model, and the extracted text is returned in Markdown format suitable for Retrieval‑Augmented Generation (RAG) pipelines.

> **Why this project?**  
> Traditional OCR libraries struggle with complex layouts, scanned documents, or images embedded in PDFs.  
> By using a large language model with vision capabilities, we can extract clean, structured text even from noisy or multi‑column PDFs.

## Features

- Convert any PDF to a sequence of Markdown‑formatted text blocks.
- Uses the OpenAI API (`gpt-4o-mini` by default) – no local OCR engine required.
- Simple command‑line interface.
- Supports custom OpenAI model, API key, and base URL.

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.9+ |
| `pdf2image` | pip install `pdf2image` |
| `openai` | pip install `openai` |
| `pillow` | pip install `pillow` |
| `poppler` (for `pdf2image` on Windows/Linux/macOS) | See [pdf2image docs](https://github.com/Belval/pdf2image) |

> **Tip:** On Windows you need to install Poppler and add its `bin` folder to your `PATH`.

## Installation

```bash
# Clone the repository
git clone https://github.com/simon3z/visionpdftext.git
cd visionpdftext

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install the package (editable mode for development)
pip install -e .
```

> The project uses a `pyproject.toml` file for dependency management.  
> If you prefer a non‑editable install, simply run `pip install .`.

## Usage

```bash
# Basic usage
visionpdftext path/to/document.pdf

# With custom API key (or set OPENAI_API_KEY env var)
visionpdftext path/to/document.pdf --api_key YOUR_KEY

# Specify a different model
visionpdftext path/to/document.pdf --model gpt-4o

# Use a custom OpenAI base URL (e.g., for Azure)
visionpdftext path/to/document.pdf --base_url https://YOUR_ENDPOINT.openai.azure.com
```

### Output

For each page, the script prints:

```
Page 1 Text:
<markdown content>

Page 2 Text:
<markdown content>
...
```

The Markdown content contains only the extracted text, no extra commentary or prompts.

## Example

```bash
visionpdftext examples/sample.pdf
```

Output:

```
Page 1 Text:
# Title

This is the first paragraph of the document...

Page 2 Text:
## Section 1

Details about section 1...
```

## Environment Variables

You can set the following environment variables instead of passing them on the command line:

- `OPENAI_API_KEY` – Your OpenAI API key.
- `OPENAI_BASE_URL` – Base URL for the OpenAI API (useful for Azure deployments).
- `OPENAI_MODEL` – Default model to use (defaults to `gpt-4o-mini`).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `poppler` not found | Install Poppler and add its `bin` directory to your `PATH`. |
| `openai` errors | Verify your API key and quota. |
| Slow processing | Each page is sent to the model individually; consider batching or using a cheaper model. |

## Contributing

Pull requests are welcome! Please open an issue first to discuss major changes.

## License

MIT © 2025 Federico Simoncelli

