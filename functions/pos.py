# -----------------------------------
# POS Tagging
# -----------------------------------

from collections import Counter
import pandas as pd
import numpy

# -----------------------------------
# POS TAGS + FREQUENCIES
# -----------------------------------

# GET_POS_TAGS()
# -----------------------------------
# SENTS = spaCy Doc.sents (https://spacy.io/api/doc#sents)
# POS_TAGGED_DICT = dict(); all individual terms (= each term once per passage) and their associated POS Tags
# POS_TAGGED_LIST = list(); all POS Tags per passage in their original order

def get_pos_tags(sents):
    pos_tagged_dict = dict()
    pos_tagged_list = list()
    counter = 0
    for sents_grouped in sents:
        pos_tagged_dict[counter] = {}
        pos_tagged_list_level1 = []
        for sentence in sents_grouped:
            for token in sentence: 
                pos_tagged_dict[counter][token.text] = token.pos_
                pos_tagged_list_level1.append(token.pos_)
        pos_tagged_list.append(pos_tagged_list_level1)
        counter += 1
    return pos_tagged_dict, pos_tagged_list

# COUNT_TAG_FREQS()
# -----------------------------------
# POS_TAGGED = list(); output POS_TAGGED_LIST from GET_POS_TAGS
# SORTED_TAG_FREQS = pd.DataFrame(); where rows = tag name, columns = index of passage, values = relative frequencies
# TAGS_USED = list(); all individual POS Tags used within an input text/document

def count_tag_freqs(pos_tagged):
    values_per_key = {}
    tags_used = [] 
    pos_counter = 0
    # absolute frequencies: iterate through all values (assigned) in pos_tagged and count the individual frequencies
    for passage in pos_tagged:
        values_per_key[pos_counter] = {}
        for token in passage:
            if token in values_per_key[pos_counter].keys():
                values_per_key[pos_counter][token] += 1
            else:
                values_per_key[pos_counter][token] = 1
            if token not in tags_used:
                tags_used.append(token)            
        pos_counter += 1 
    # relative frequencies: based on number of words within one passage
    num_words = 0
    for tagset in values_per_key.values():
        num_words = sum(tagset.values())
        for k, v in tagset.items():
            rel_freq = v / num_words
            tagset[k] = rel_freq
    sorted_tag_freqs = pd.DataFrame(values_per_key).sort_index()
    return sorted_tag_freqs, tags_used


# -----------------------------------
# RETURN POS N-GRAMS
# -----------------------------------

# FIND_NGRAM_INDEX()
# -----------------------------------
# POS_TAGGED = list(); output POS_TAGGED_LIST from GET_POS_TAGS
# NGRAM = str(); in the form "[pos_tag],[pos_tag_2],[pos_tag_n]"
# INDEX_LIST = list()

def find_ngram_index(pos_tagged, ngram):
    ngram = ngram.replace(" ","")
    index_list = []
    counter = 0
    for nested_list in pos_tagged:
        tag_str= ""
        for tag in nested_list:
            tag_str += tag 
            tag_str += ","
        if ngram in tag_str:
            index_list.append(counter)
        counter += 1
    return index_list

# FIND_NGRAMS()
# -----------------------------------
# POS_TAGGED = list(); output POS_TAGGED_LIST from GET_POS_TAGS
# N = int(); n as in n-Gram
# NGRAMS_LIST = list(); all the corresponding n-Grams found

def find_ngrams(pos_tagged, n):
    ngrams_list = []
    for nested_list in pos_tagged:
        #element_list = list(element)
        for item in range(len(nested_list)-n):
            every_ngram = []
            for i in range(item, item+n, +1):
                every_ngram.append(nested_list[i])
            ngrams_list.append(every_ngram)
    return ngrams_list

#NGRAM_COUNT()
# -----------------------------------
# NGRAMS = list(); output NGRAMS_LIST from FIND_NGRAMS
# DF = pd.Dataframe(); cols = ["ngram", "count"]

def ngram_count(ngrams):
    ngram_counter = Counter((tuple(item) for item in ngrams))
    df = pd.DataFrame.from_dict(ngram_counter, orient='index').reset_index()
    df = df.rename(columns={'index':'ngram', 0:'count'})
    df = df.sort_values(by=['count'], ascending=False)
    df.ngram = df.ngram.astype("str")
    return df

# GET_N_NGRAMS()
# -----------------------------------
# N = list([int_1, int_2, int_n]); n as in n-Gram
# TOPN = int(); how many highest values to return
# POS_TAGGED = list(); output POS_TAGGED_LIST from GET_POS_TAGS
# NGRAMS = list() of pd.Dataframes(); for each n returns a df similar to output DF from NGRAM_COUNT() 
# NAMES = list(); contains names for each of the nested dfs to use for vis

def get_n_ngrams(n, topn, pos_tagged):
    if isinstance(n, list):
        ngrams = []
        names = []
        for number in n:
            ngram = ngram_count(find_ngrams(pos_tagged, number))
            ngrams.append(ngram[:topn])
            names.append(str(number) + "-grams")
    else: 
        ngrams = ngram_count(find_ngrams(pos_tagged, n))
        names = [str(n) + "-grams"]
    return ngrams, names


# -----------------------------------
# COMPARE POS N-GRAMS
# -----------------------------------

# LIST_INDIVIDUAL_GRAMS()
# -----------------------------------
# DF_LISTS = list() of pandas.DataFrames(); output NGRAMS created by GET_N_NGRAMS()
# ALL_GRAMS_LIST = list(); all individual ngrams over the different input DataFrames

def list_individual_grams(df_lists):
    all_grams_list = []
    for grams_list in df_lists:
        for sublist in grams_list:
            for gram in sublist.ngram:
                val_index = sublist.ngram[sublist.ngram == gram].index.values
                if val_index <= 1:
                    pass
                elif gram in all_grams_list:
                    pass
                else:
                    all_grams_list.append(gram)
    return all_grams_list

# GRAMS_MATRIX_PREP()
# -----------------------------------
# GRAMS = list() of pandas.DataFrames(); output NGRAMS created by GET_N_NGRAMS()
# ALL_GRAMS = list(); output ALL_GRAMS_LIST from LIST_INDIVIDUAL_GRAMS()
# TYPE = str(); either "binary" or "count" -> add check type before execution in the future
# CHECK_GRAMS = returns list of binary values/count for each n-gram in all_grams

def grams_matrix_prep(grams, all_grams, type):
    df = pd.concat(grams, ignore_index=True)
    check_grams = []
    for all_gram in all_grams:
        if all_gram in list(df.ngram):
            if type == "binary":
                check_grams.append(1)
            if type == "count":
                val_index = df.ngram[df.ngram == all_gram].index.values
                check_grams.append(df.loc[val_index, "count"].values[0])
        else:
            check_grams.append(0)
    return check_grams


# -----------------------------------
# POS DIVERSITY
# -----------------------------------

# GET_POS_DIVERSITY()
# -----------------------------------
# DF = pandas.DataFrame; output SORTED_TAG_FREQS from COUNT_TAG_FREQS()
# DIV_DF = pandas.DataFrame; contains column "pos_diversity" (Shannon Entropy for all POS Tag frequencies per passage)

def get_pos_diversity(df):
    list_vals = []
    for col in df.columns:
        diversity_sum = 0
        tag_vals = []
        for tag in df[col]:
            if numpy.isnan(tag):
                pass
            else:
                diversity = tag * numpy.log2(tag)
                tag_vals.append(diversity)
        for val in tag_vals:
            diversity_sum += val
        list_vals.append(-diversity_sum if diversity < 0 else diversity_sum) # added condition "if diversity < 0 else diversity_sum" here to change -0 values to 0
        div_df = pd.DataFrame(list_vals, columns=['pos_diversity'])
    return div_df

# -----------------------------------
# POS TAGS GLOSSARY
# -----------------------------------
    
# look up all existing possible pos tags: https://github.com/explosion/spaCy/blob/master/spacy/glossary.py
# used here: only universal & german pos tags so far

def get_pos_glossary(): 
    pos_glossary = {
        # POS tags
        # Universal POS Tags
        # http://universaldependencies.org/u/pos/
        "ADJ": "adjective",
        "ADP": "adposition",
        "ADV": "adverb",
        "AUX": "auxiliary",
        "CONJ": "conjunction",
        "CCONJ": "coordinating conjunction",
        "DET": "determiner",
        "INTJ": "interjection",
        "NOUN": "noun",
        "NUM": "numeral",
        "PART": "particle",
        "PRON": "pronoun",
        "PROPN": "proper noun",
        "PUNCT": "punctuation",
        "SCONJ": "subordinating conjunction",
        "SYM": "symbol",
        "VERB": "verb",
        "X": "other",
        "EOL": "end of line",
        "SPACE": "space",
        # POS Tags (German)
        # TIGER Treebank
        # http://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/TIGERCorpus/annotation/tiger_introduction.pdf
        "$(": "other sentence-internal punctuation mark",
        "$,": "comma",
        "$.": "sentence-final punctuation mark",
        "ADJA": "adjective, attributive",
        "ADJD": "adjective, adverbial or predicative",
        "APPO": "postposition",
        "APPR": "preposition; circumposition left",
        "APPRART": "preposition with article",
        "APZR": "circumposition right",
        "ART": "definite or indefinite article",
        "CARD": "cardinal number",
        "FM": "foreign language material",
        "ITJ": "interjection",
        "KOKOM": "comparative conjunction",
        "KON": "coordinate conjunction",
        "KOUI": 'subordinate conjunction with "zu" and infinitive',
        "KOUS": "subordinate conjunction with sentence",
        "NE": "proper noun",
        "NNE": "proper noun",
        "PAV": "pronominal adverb",
        "PROAV": "pronominal adverb",
        "PDAT": "attributive demonstrative pronoun",
        "PDS": "substituting demonstrative pronoun",
        "PIAT": "attributive indefinite pronoun without determiner",
        "PIDAT": "attributive indefinite pronoun with determiner",
        "PIS": "substituting indefinite pronoun",
        "PPER": "non-reflexive personal pronoun",
        "PPOSAT": "attributive possessive pronoun",
        "PPOSS": "substituting possessive pronoun",
        "PRELAT": "attributive relative pronoun",
        "PRELS": "substituting relative pronoun",
        "PRF": "reflexive personal pronoun",
        "PTKA": "particle with adjective or adverb",
        "PTKANT": "answer particle",
        "PTKNEG": "negative particle",
        "PTKVZ": "separable verbal particle",
        "PTKZU": '"zu" before infinitive',
        "PWAT": "attributive interrogative pronoun",
        "PWAV": "adverbial interrogative or relative pronoun",
        "PWS": "substituting interrogative pronoun",
        "TRUNC": "word remnant",
        "VAFIN": "finite verb, auxiliary",
        "VAIMP": "imperative, auxiliary",
        "VAINF": "infinitive, auxiliary",
        "VAPP": "perfect participle, auxiliary",
        "VMFIN": "finite verb, modal",
        "VMINF": "infinitive, modal",
        "VMPP": "perfect participle, modal",
        "VVFIN": "finite verb, full",
        "VVIMP": "imperative, full",
        "VVINF": "infinitive, full",
        "VVIZU": 'infinitive with "zu", full',
        "VVPP": "perfect participle, full",
        "XY": "non-word containing non-letter",
        }
    return pos_glossary