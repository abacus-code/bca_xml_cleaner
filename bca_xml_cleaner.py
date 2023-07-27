'''
XML cleaner: removes tabs and newlines from XML data
'''
import argparse
import os
import pathlib
import textwrap
import re
import sys

VERSION = (0, 2, 3)
__version__ = '.'.join([str(x) for x in VERSION])

def parsley()->argparse.ArgumentParser:
    '''
    Argument parser
    '''
    description = '''
                  XML cleaner. Will remove newlines and tabs from XML data so that when you
                  export it to another format, like, say, CSV, it won't break the output.

                  This may take a long time, especially with gigantic XML files.
                  '''
    block_size = '''
                Minimum number of characters to read per block. The utility will
                read this many plus any extra to reach the end of the next tag –
                ie. the '>' character. Assuming one byte per character, the default
                of 536870912 will read and write XML data in approximately 0.5 GB
                chunks, which should save your RAM and drive.
                '''
    humanread =  '''
                 Human readable text — one tag group per line. If you want more
                 than one line of text, use this option. By default the XML
                 output will be a single line of text unless you use this switch.
                 '''
    encod = '''
            Encoding of the input file. Defaults to UTF-8. Output will always be
            UTF-8 because Windows-specific encodings are irritating.
            '''
    outy = '''
           Output file. If not supplied, output defaults to stdout.
           '''
    parser = argparse.ArgumentParser(description=textwrap.dedent(description),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-b', '--blocksize',
                        help = textwrap.dedent(block_size)[1:],
                       default=536870912)
    parser.add_argument('-e', '--encoding',
                        help = textwrap.dedent(encod)[1:],
                       default='utf-8')
    parser.add_argument('-r', '--readable',
                       action='store_true',
                        help = textwrap.dedent(humanread)[1:])
    parser.add_argument('infile',
                       help = 'XML file to process')
    parser.add_argument('-o','--outfile',
                        help= textwrap.dedent(outy)[1:],
                        default=None)
    parser.add_argument('-v','--version', action='version',
                        version='%(prog)s '+__version__,
                        help='Show version number and exit')
    return parser

def process_file(infile:pathlib.Path,
                 outfile:str,
                 blocksize:int, encoding='utf-8',
                 humr=False)->None:
    '''
    Replaces tabs and newlines in an XML file, plus
    removes occurences of multiple spaces.
    infile: pathlib.Path
        The incoming xml file.
    outfile: str
        The outgoing cleaned file. Because None as a value
        causes output to stdout, this input should be a string
        or None.
    blocksize: int
        Minimum number of characters to read, approximately
        equal to the number of bytes.
    humr:bool
        Human-readability flag.
    '''
    #Remove any extra spaces because you shouldn't have these
    spc = re.compile('\s\s+')#pylint: disable=anomalous-backslash-in-string
    #By default the chunks append, so it's necessary to erase the file
    #in case you do need to process it more than once
    if outfile:
        outfile = pathlib.Path(outfile)
        if os.path.exists(outfile):
            os.remove(outfile)
    with open(infile, 'r', encoding=encoding) as fil:
        data  = fil.read(blocksize) # Stream the file in
        while data:
            #read to end of a tag
            while not data.endswith('>'):
                add = fil.read(1)
                data = data + add
                if not add:
                    break # You have reached the end
            # Tab and \n are the problematic characters
            data = data.strip().replace('\t', ' ').replace('\n', ' ')
            #remove two or more spaces
            data = ' '.join([x for x in re.split(spc, data) if x])
            # For human readability
            if humr:
                data = data.replace('> <', '>\n<')
            # write/append file after every 0.5 GB read so that the buffer doesn't
            # exceed memory capacity
            if not outfile: # explicit stdout in case of platform weirdness
                print(data, file=sys.stdout)
            else:
                with open(outfile, 'a+', encoding='utf-8', newline='') as outf:
                    outf.write(data)
            #And start with a new block
            data  = fil.read(blocksize)

def main():
    '''
    You know what this is.
    '''
    args = parsley().parse_args()
    process_file(pathlib.Path(args.infile),
                 args.outfile,
                 args.blocksize,
                 args.encoding,
                 args.readable)

if __name__ == '__main__':
    main()
