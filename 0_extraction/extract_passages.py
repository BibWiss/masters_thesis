"""
usage: extract_passages.py [-h] [-o {.csv,.pkl}] -c {.json} -t {.txt}

A small program to extract key passage texts based on their (start/end)
position in the text.

optional arguments:
  -h, --help            show this help message and exit
  -o {.csv,.pkl}, --output {.csv,.pkl}
                        Output path/file name

required named arguments:
  -c {.json}, --citations {.json}
                        citation_sources path/file name
  -t {.txt}, --text {.txt}
                        literary text path/file name
"""
import argparse

import json
import pandas as pd

# import segment types from key_passager

from key_passager.CitationSource import CitationSource
from key_passager.ImportantSegment import ImportantSegment
from key_passager.SourceSegment import SourceSegment

#from Choices import Choices
# above does only work if relative path is used, therefore solution below for now

class Choices():
    def __init__(self, *choices):
        self.choices = choices

    def __contains__(self, choice):
        # True if choice ends with one of self.choices
        return any(choice.endswith(c) for c in self.choices)

    def __iter__(self):
        return iter(self.choices)

# set arguments to parse for CLI usage (argparse)
kp_parser = argparse.ArgumentParser(description="A small program to extract key passage texts based on their (start/end) position in the text.")
kp_parser.add_argument('-o', '--output', help='Output path/file name', default="output.csv", choices=Choices(".csv", ".pkl"))
requiredNamed = kp_parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-c', '--citations', help='citation_sources path/file name', choices=Choices(".json"), required=True)
requiredNamed.add_argument('-t', '--text', help='literary text path/file name', choices=Choices(".txt"), required=True)

args = kp_parser.parse_args()
citation_sources_path = args.citations
literary_text_path = args.text
output_file = args.output

# processing key passages, larger parts taken from Characterizer.py by Frederik Arnold

# define segment types from above and return them + information
def __json_decoder_citation_source(json_input):
    if 'source_segments' in json_input:
        return CitationSource(json_input['my_id'], json_input['source_segments'], json_input['important_segments'],
                              json_input['text'])
    elif 'source_segment_ids' in json_input:
        return ImportantSegment(json_input['my_id'], json_input['source_segment_ids'], json_input['frequency'],
                                json_input['token_length'], json_input['text'])
    else:
        return SourceSegment(json_input['my_id'], json_input['start'], json_input['end'], json_input['frequency'],
                             json_input['token_length'], '')

# read json and apply json_decoder

with open(citation_sources_path, 'r', encoding='utf-8') as citation_sources_file:
        citation_sources = json.load(citation_sources_file, object_hook=__json_decoder_citation_source)

# create dataframe by looping over citation_sources and appending the values to a dictionary as in https://www.kite.com/python/answers/how-to-append-rows-to-a-pandas-dataframe-using-a-for-loop-in-python

columns=['id','startpos','endpos']
data = []

passage_freqs = []

# get the first and last position of each source_segments element

for citation_source in citation_sources:

    values = [citation_source.my_id, citation_source.source_segments[0].start, citation_source.source_segments[-1].end]
    zipped = zip(columns, values)
    data_dictionary = dict(zipped)
    data.append(data_dictionary)
    #add frequency per citation_source
    length = len(citation_source.source_segments)
    freqs_per_cs = [citation_source.source_segments[i].frequency for i in range(length)]
    freqs_sum = 0
    for freq in freqs_per_cs:
        freqs_sum += freq
    rel_freq = freqs_sum / length
    passage_freqs.append(rel_freq)
    
df = pd.DataFrame()
df = df.append(data, True)
df = df.assign(frequency=passage_freqs) 

# rewrite, not a good way to create df cols
df["text"] = ""

# open literary text

with open(literary_text_path, "r", encoding="utf-8") as literary_text_file:
    literary_text = literary_text_file.read()

# loop over the df rows and get startpos/endpos of every entry

def get_kp(col):
    for index, row in df.iterrows():
        startpos = int(row[1])
        endpos = int(row[2])
        col.loc[index] = literary_text[startpos:endpos]

get_kp(df["text"])

print(df.head())

# save it

if output_file[-4:] == ".pkl":
    df.to_pickle(output_file)
else:
    df.to_csv(output_file, header=True)