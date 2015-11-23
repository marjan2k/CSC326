import re

def split_sentence(file_name):
     text = open(file_name).read()
     text = text.replace('\n', ' ').replace('\r', '')
     m = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', text)
     for i in m:
         print i

if __name__ == "__main__":
    split_sentence("smith.txt")
