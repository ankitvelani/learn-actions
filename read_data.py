import os


arr = os.listdir()
print(arr)
file_name = "sample.log"
with open(file_name, encoding='utf8') as f:
    for line in f:
        print(line.strip())
