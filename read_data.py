import os

file_name = os.environ.get('LOG_FILE')
with open(file_name, encoding='utf8') as f:
    for line in f:
        print(line.strip())
