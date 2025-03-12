import ollama

res = ollama.list()
# this will give the all models list
# print(res)  

import ollama

prompt =''' 

<<<ERROR_LOG>>>


CMN_1154 [Database driver event...Error occurred loading library [libsapnwrfc.so: cannot open shared object file: No such file or directory]Database driver event...Error occurred loading library [libpmsaprdr.so]]

<<<END_ERROR_LOG>>>

Analyze the provided log data to identify the errors and their root causes. Use the Informatica Knowledge Base and relevant documentation as a reference to provide possible solutions for each error. Ensure that the explanation includes:

Error Status: Return True or False, return True if it's really an error, and False if it's not an error (e.g., just showing no error, zero error, or informational message).

Error Related Platform: Full name of the software/database/platform (e.g., Informatica PowerCenter, Informatica Data Management Cloud,  or any database) with possible versions related to this error.

Error Statement: Provide the raw error you received.

Error Identification: Extract and clearly state the error message, error code, and context.

Root Cause Analysis: Identify what might have caused the error, referencing potential issues such as missing columns, incorrect SQL syntax, or misconfigured connections.

Proposed Solutions: Suggest specific steps to resolve the error, including:
- Verifying database schemas or columns.
- Correcting SQL statements.
- Configuring Informatica mappings or transformations.
- Checking SQL and providing the correct one if the SQL syntax is wrong.
- Any other related solutions.

Validation: Provide steps to validate the resolution and ensure the issue is fixed.


Error Severity :Assess the impact on the ETL process and mappings Choose any one: Low – Minor issue, does not disrupt ETL execution. Medium – Partial failure,affects some mappings but not the entire workflow. High – Major issue, causes ETL failure or incorrect data processing. 

Responsible Team : Which team should the ticket be raised to? Choose one from the following: Database Team, Development Team, System Team, or Testing Team.

Provide all these solutions as a dictionary of lists.

Do not provide any additional text, only the dictionary of lists.
'''
response = ollama.chat(
    model="gemma:2b",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": prompt},
    ]
    ,
    stream=False
)

# print(response)

print(response['message']['content'])



#uncomment it if the stream=True
# for res in response :
#     print(res['message']['content'],end='',flush=True)





