
from openai import OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders
from dotenv import load_dotenv
import os

client = OpenAI(
    api_key="dunmy",#openai-apikey
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(
        provider=os.getenv("AI_PROVIDER"),
        virtual_key=os.getenv("PORTKEY_VIRTUAL_KEY"),
        api_key=os.getenv("PORTKEY_API")
    )
)

chat_complete = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's a Fractal?"}],
)

print(chat_complete.choices[0].message.content)

