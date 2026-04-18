from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
prompt = "Hello, how are you?"
completion = client.chat.completions.create(
model="openai/gpt-oss-120b",
messages=[
{
"role": "user", "content": prompt
}
]
)

print(completion.choices[0].message.content)
