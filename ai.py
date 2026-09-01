import os
from google import genai

# Retrieve secret/environment variable
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_image(image_path):
    # Read the image data, "rb" means read binary. 
    with open(image_path, "rb") as f:
        image_data = f.read()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": image_data,
                }
            },
            """
            You are an AI security camera analyzing a motion-triggered image.

            Describe only information relevant to a security event.

            Report:
            - Whether a person is present
            - Whether an animal is present
            - What significant objects or activity are visible
            - What the person or animal appears to be doing
            - Any obvious security-relevant event

            Do not identify or infer the person's identity.
            Do not describe sensitive personal characteristics.
            Be concise and factual.

            If nothing security-relevant is happening, say so.
            """,
        ],
    )

    return response.text