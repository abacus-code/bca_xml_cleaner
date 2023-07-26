'''
XML cleaner: removes tabs and newlines from XML data
'''
import os
import pathlib
import re

INFILE = '20230331_REVD23_0180.xml'
#INFILE = 'dummy.xml'
infile = pathlib.Path(INFILE)
OUTFILE = 'cleaned.xml'
file = pathlib.Path(OUTFILE)
BLOCK = 536870912 #0.5GB block size, so that you don't run out of RAM
spc = re.compile('\s\s+')
if os.path.exists(file):
    os.remove(file)
#with open('dummy.xml', 'r', encoding='utf-8') as f:
with open(infile, 'r', encoding='utf-8') as f:
    data  = f.read(BLOCK) # Stream the file in
    while data:
        #read to end of a tag
        while not data.endswith('>'):
            add = f.read(1)
            data = data + add
            if not add:
                break # You have reached the end
        # Tab and \n are the problematic characters
        data = data.strip().replace('\t', ' ').replace('\n', ' ')
        #remove two or more spaces
        data = ' '.join([x for x in re.split(spc, data) if x])
        # For human readability
        data = data.replace('> <', '>\n<')
        # write/append file after every 0.5 GB read so that the buffer doesn't
        # exceed memory capacity
        with open(file, 'a+', encoding='utf-8', newline='') as outf:
            outf.write(data)
        #And start with a new block
        data  = f.read(BLOCK)

