import ollama

response = ollama.generate(
    model="gemma:2b",
    prompt="Tell me about black holes.",
    stream=False
)
#Use the lines below if the stream=False
print(response['response'])

#Use the lines below if the stream=True
# for res in response :
#     print(res['response'],end='',flush=True)


