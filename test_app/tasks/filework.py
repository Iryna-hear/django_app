import os
script_dir = os.path.dirname(__file__)




# file = open('filepath', 'r', encoding='utf-8')
# file.close()
"""
r = read 
w = write
a = add
rb = read binary
wb = write binary
r+ = read and write
"""

filepath = os.path.join(script_dir, 'simple.txt')
# file_content = 'Hello, this is a simple text file.\n'
# with open(filepath, 'a', encoding='utf-8') as file:
#     content = file.write(file_content)


with open(filepath, 'r', encoding='utf-8') as file:
    content_readlines = file.readlines()
    print(f'readlines: {content_readlines}')

    content_read = file.read()
    print(f'read: {content_read}')

#   for line in file:
#     print(line.strip())  