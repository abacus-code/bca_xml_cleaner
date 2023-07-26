'''
XML cleaner: removes tabs and newlines from XML data
'''
import argparse
import os
import pathlib
import textwrap
import re

VERSION = (0, 1, 0)
version = '.'.join([str(x) for x in VERSION])

def parsley()->argparse.ArgumentParser:
    '''
    Argument parser
    '''
    description = '''
                  XML cleaner. Will remove newlines and tabs from XML data so that
                  when you export it to another format, like, say, CSV, it won't
                  break the output
                  '''
    blocksize = '''
                Minimum number of characters to read per block. The utility will
                read this many plus any extra to reach the end of the next tag,
                ie the '>' character. Assuming one byte per character, the default
                of 536870912 will read and write XML data in approximately 0.5 GB
                chunks, which should save your RAM and drive.
                '''
    humanread =  '''
                 Human readable text — one tag group per line. If you want more
                 than one line of text, use this option.
                 '''
    parser = argparse.ArgumentParser(description=textwrap.dedent(description),
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-b', '--blocksize',
                       help = textwrap.dedent(blocksize),
                       default=536870912,
                       required = False)
    parser.add_argument('-r', '--readable',
                       action='store_true',
                       help = textwrap.dedent(humanread))
    parser.add_argument('infile',
                       help = 'XML file to process')
    parser.add_argument('outfile',
                          help= 'Output file')
    return parser


def main():
    '''
    Call this to make it work
    '''
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

def test():
    args = parsley().parse_args()
    print(args)

if __name__ == '__main__':
    test() 
