# bca_xml_cleaner

XML cleaner; removes tabs and newlines from XML data

## Introduction

[BC Assessment data](https://catalogue.data.gov.bc.ca/dataset/bc-assessment-data-advice), notably but probably not exclusively in its _Data Advice_ product, is supplied to end users like the BC provincial government and universities in plain XML format. The XML files are used as a basis for other, more user-friendly formats, such as comma-separated value tables.

Unfortunately, the data as supplied in the XML can have issues which affect its usability in other formats – notably, some of the fields contain newlines, tabs and commas which for obvious reasons can affect plain text formats such as comma-separated value files.

There are a number of ways to work around this problem.

## Options

* Data products are provided as a geopackage (ie, .gpkg), which is a [SQLite](https://sqlite.org) database. This format doesn't remove any of the issues, but the fields are parsed correctly because databases generally don't care if there are commas, newlines, tabs, etc in the data. This, though, is only useful for researchers familiar with geospatial databases.

At the very least, the geopackage data can be used to identify which records have issues, as it's possible to easily search the database for problematic characters.

* The *best* way to avoid this problem is to stop it before it starts; that is to remove the problematic characters from the raw XML *before* making other formats. While simple enough in theory, many users would have difficulty loading, let alone processing, a text file which weighs in at over 16 GB.

## Solution

Although hardly super-fast, the Python script included here will easily remove line breaks and tabs from *any* XML data. Because not everyone has enough RAM for processing a huge file, the script will process data in user-configurable streaming chunks (default 0.5 GB). The output file can be made "human-readable" (one tag and data group per line) or just concatenated into a single line. Machines don't care about human-readability.

## Usage

Run the script `bca_xml_cleaner.py` with `python3 bca_xml_cleaner.py`. No extra bells and whistles are needed; everything is included in the Python standard library.

```nohighlight
usage: bca_xml_cleaner.py [-h] [-b BLOCKSIZE] [-e ENCODING] [-r] [-o OUTFILE] [-v] infile

XML cleaner. Will remove newlines and tabs from XML data so that when you
export it to another format, like, say, CSV, it won't break the output.

This may take a long time, especially with gigantic XML files.

positional arguments:
  infile                XML file to process

options:
  -h, --help            show this help message and exit
  -b BLOCKSIZE, --blocksize BLOCKSIZE
                        Minimum number of characters to read per block. The utility will
                        read this many plus any extra to reach the end of the next tag –
                        ie. the '>' character. Assuming one byte per character, the default
                        of 536870912 will read and write XML data in approximately 0.5 GB
                        chunks, which should save your RAM and drive.
  -e ENCODING, --encoding ENCODING
                        Encoding of the input file. Defaults to UTF-8. Output will always be
                        UTF-8 because Windows-specific encodings are irritating.
  -r, --readable        Human readable text — one tag group per line. If you want more
                        than one line of text, use this option. By default the XML
                        output will be a single line of text unless you use this switch.
  -o OUTFILE, --outfile OUTFILE
                        Output file. If not supplied, output defaults to stdout.
  -v, --version         Show version number and exit
```
