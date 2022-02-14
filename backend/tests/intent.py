import json

file_content = None

with open("annotated_queries.json") as file:
    file_content = json.load(file)

print(file_content)