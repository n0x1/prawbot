from groq import Groq
import os


client = Groq(
    api_key="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"
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat_completion.choices[0].message.content)