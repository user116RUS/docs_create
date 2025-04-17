from openai import OpenAI

client = OpenAI(
    api_key="sk-or-vv-9d90950af188ed57252dbbc413034c8038f982ddf17e9f6d187e2ca03c227f3f",
    base_url="https://api.vsegpt.ru/v1",
)

prompt = ("")

messages = []
#messages.append({"role": "system", "content": system_text})
messages.append({"role": "user", "content": prompt})

response_big = client.chat.completions.create(
    model="openai/gpt-4o-mini", # id модели из списка моделей - можно использовать OpenAI, Anthropic и пр. меняя только этот параметр
    messages=messages,
    temperature=0.7,
    n=1,
    max_tokens=3000, # максимальное число ВЫХОДНЫХ токенов. Для большинства моделей не должно превышать 4096
    extra_headers={ "X-Title": "My App" }, # опционально - передача информация об источнике API-вызова
)

#print("Response BIG:",response_big)
response = response_big.choices[0].message.content
print("Response:", response)