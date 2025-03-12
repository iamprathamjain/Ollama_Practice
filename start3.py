import ollama

# Initialize chat history
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

# User asks first question
messages.append({"role": "user", "content": "Tell me a joke about AI."})
response = ollama.chat(model="gemma:2b", messages=messages)

# Store AI response
messages.append({"role": "assistant", "content": response['message']['content']})
print("AI:", response['message']['content'])

# User asks another question
messages.append({"role": "user", "content": "Haha! Now, tell me a fun fact about space."})
response = ollama.chat(model="gemma:2b", messages=messages)

# Store AI response and print
messages.append({"role": "assistant", "content": response['message']['content']})
print("AI:", response['message']['content'])
