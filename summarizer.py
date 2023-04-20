# Source: https://github.com/dayrev/smmry-sdk-php

"""


MIT License

Copyright (c) Daniel Sposito

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

#!/usr/bin/python3
import argparse
import os
import sys
import requests
import json

# get your api key from: https://smmry.com/api
SMMRY_API_KEY='YOUR_API_KEY'
SMMRY_URL='https://api.smmry.com/'

def summarizeText(text):
    url=SMMRY_URL+'&SM_API_KEY='+SMMRY_API_KEY
    headers={
    'Expect':''
    }
    response=requests.post(url, data={'sm_api_input':text}, headers=headers)
    summary=json.loads(response.content.decode('utf-8'))
    return summary

def summarizeFile(file):
    print("Input file is: {}".format(args.ifile.name))
    fileText=args.ifile.read()
    return summarizeText(fileText)

def summarizeURL(url):
    print("URL to summarize is: {}".format(args.url))
    url=SMMRY_URL+'&SM_API_KEY='+SMMRY_API_KEY+'&SM_URL='+args.url
    response=requests.get(url)
    summary=json.loads(response.content.decode('utf-8'))
    return summary

def summarizeStdin():
    inp=input("Using standard input for summary. Type the text you want to summarize:")
    return summarizeText(inp)

parser = argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
group.add_argument('-i', '--ifile', type=argparse.FileType('r'), help='Input file to summarize')
group.add_argument('-u', '--url', help='URL of page to summarize')
parser.add_argument('-o', '--ofile', type=argparse.FileType('w', encoding='UTF-8'), help='Output file')

"""args = parser.parse_args()
if args.ifile:
    summary=summarizeFile(args.ifile)
elif args.url:
    summary=summarizeURL(args.url)
else:
    summary=summarizeStdin()
if args.ofile:
    print("Summary was written to: {}".format(args.ofile.name))
    args.ofile.write(summary)
else:
    print("The summarized text is:\n{}".format(summary))"""