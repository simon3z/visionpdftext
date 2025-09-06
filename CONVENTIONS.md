# Introduction
This is a python project about converting pdf documents to images so they can be processed by LLM with vision capability in order to more effectively convert them to text.

# Converting PDF to Images

Example:

```python
from pdf2image import convert_from_path

images = convert_from_path('example.pdf')

for i in range(len(images)):
    images[i].save('page'+ str(i) +'.png', 'PNG')
```


# Images Conversion in Memory

Example:

```python
from io import BytesIO

membuf = BytesIO()
image.save(membuf, format="png")
```


# Using Images with OpenAI API

Example:

```python
import base64
from openai import OpenAI

client = OpenAI()

prompt = "What is in this image?"
with open("path/to/image.png", "rb") as image_file:
    b64_image = base64.b64encode(image_file.read()).decode("utf-8")

response = client.responses.create(
    model="gpt-4o-mini",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": f"data:image/png;base64,{b64_image}"},
            ],
        }
    ],
)
```
