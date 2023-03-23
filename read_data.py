import os


arr = os.listdir()
print(arr)
file_name = "sample.log"
with open(file_name, encoding='utf8') as f:
    for line in f:
        print(line.strip())


with open('file1.txt', 'w') as f:
    print('hello world', file=f)
