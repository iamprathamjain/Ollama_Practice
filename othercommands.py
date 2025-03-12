import ollama

# Define a Modelfile as a multi-line string
MODELFILE_CONTENT = """ 
# Base model
FROM gemma:2b

# Parameters
PARAMETER temperature=0.7

# System Prompt
SYSTEM 
You are an AI assistant trained to provide detailed answers.


# Customizing model behavior
MESSAGE 
You should always be polite and provide concise answers.
"""


# Save the Modelfile content to a file

# Create a new model using the Modelfile
# ollama.create(model='knowitall',modelfile=MODELFILE_CONTENT)  # i dont know why its not working




