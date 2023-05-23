# secret key is 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

import openai
openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}
  ]
)

print(completion.choices[0].message.content)
