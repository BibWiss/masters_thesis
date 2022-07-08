"""
usage: group_passages.py [-h] [-w WORK] -i {.pkl} -t {.txt}

This Python script allows us to divide our literary text into two groups - one consisting of potential key passages ('cited') and one containing the rest ('not cited').

optional arguments:
  -h, --help            show this help message and exit
  -w WORK, --work WORK  title of the work, used for output file names

required named arguments:
  -i {.pkl}, --input {.pkl}
                        input path/file name
  -t {.txt}, --text {.txt}
                        literary text path/file name
"""

import argparse
import pandas as pd

class Choices():
    def __init__(self, *choices):
        self.choices = choices

    def __contains__(self, choice):
        # True if choice ends with one of self.choices
        return any(choice.endswith(c) for c in self.choices)

    def __iter__(self):
        return iter(self.choices)

parser = argparse.ArgumentParser(description="This Python script allows us to divide our literary text into two groups - one consisting of potential key passages ('cited') and one containing the rest ('not cited').")
parser.add_argument('-w', '--work', help='title of the work, used for output file names', default="work", type=str)
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--input', help='input path/file name', choices=Choices(".pkl"), required=True)
requiredNamed.add_argument('-t', '--text', help='literary text path/file name', choices=Choices(".txt"), required=True)

args = parser.parse_args()
work_title = args.work
inputfile = args.input
literary_text_path = args.text

# read files

df = pd.read_pickle(inputfile)

with open(literary_text_path, "r", encoding="utf-8") as literary_text_file:
    literary_text = literary_text_file.read()

# function to get specific passages

def get_passages(start_list, end_list, freq_list, passage_type):
    #f = open(file_name, mode="w", encoding="utf-8")
    passages_list = []
    for start, end in zip(start_list, end_list):
      passages_type = passage_type
      passages_list.append(literary_text[start:end])
    passages_df = pd.DataFrame({"text": passages_list, "startpos": start_list, "endpos": end_list, "frequency": freq_list, "passage_type": passages_type})
    return passages_df
      #passages_df.to_pickle(file_name)
      #f.write('"' + literary_text[start:end] + '";\n')
    #print("Successfully created file " + file_name + " for all " + passage_type + ".")

# get all KPs

KPs_start = [x for x in df['startpos']]
KPs_end = [x for x in df['endpos']] 
KPs_freq = [x for x in df['frequency']]
KP_filename = work_title + "_all-kp.pkl"
# add the corresponding passages to a txt doc, using the format: "[KP1]" ; "[KP2]" ; ... , "[KPn]"

kps = get_passages(KPs_start, KPs_end, KPs_freq, "cited")

# get all NKPs
# 0 until KP1[startpos-1], then KP1[endpos + 1] until KP[startpos-1], ... 

#define start and end positions of the document, then loop over each start-/endpos except if they are the same as start_of_doc/end_of_doc

NKPs_start = [x for x in df['endpos']] # x+1
NKPs_end =  [x if x == 0 else x for x in df['startpos']]#[x-1 for x in df['startpos']]

# check whether start and end in lists are identical to start_of_doc/end_of_doc and if they are not

start_of_doc = 0
end_of_doc = len(literary_text)

if NKPs_start[-1] == end_of_doc:
  # if doc ends with a key passage, then delete the last start entry
  NKPs_start.pop()
else:
  NKPs_end.append(end_of_doc)

if NKPs_end[0] == start_of_doc:
  # if doc starts with key passage, we do not need the first end entry
  NKPs_end = NKPs_end[1:]
elif NKPs_end[0] == NKPs_start[0]:
  # this normally happens when end 0 is dropped (condition above) 
  NKPs_end = NKPs_end[1:]
else:
  # if doc starts not with a key passage, add 0 as first start entry
  NKPs_start.insert(0, start_of_doc)



NKP_filename = work_title + "_all-nkp.pkl"

nkps = get_passages(NKPs_start, NKPs_end, 0, "not_cited")

# merge dfs
all_passages = kps.append(nkps)
all_passages_sorted = all_passages.sort_values(by="startpos")

# delete values where startpos > endpos
for index, row in all_passages_sorted.iterrows():
  if row[1] > row[2]:
    all_passages_sorted = all_passages_sorted.drop(index)

all_passages_sorted = all_passages_sorted.reset_index(drop=True)
print(all_passages_sorted.head())
all_passages_sorted.to_csv("j_all.csv", index=False)
all_passages_sorted.to_pickle("j_all.pkl")
