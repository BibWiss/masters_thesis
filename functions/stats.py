# -----------------------------------
# FUNCTIONS FOR FREQUENCY-/DISTRIBUTION-BASED STATISTICAL ANALYSIS
# -----------------------------------

from .processing import tokenize_text
import pandas as pd
import inspect

# -----------------------------------
# TEXT MEASURES
# -----------------------------------

# GET_CHAR_LEN()
# -----------------------------------
# TEXT = str() or list()
# CHAR_LEN_LISTED = int() or list(); depending on input

def get_char_len(text):
    # check whether to treat input as list or simple text
    if isinstance(text, list): 
        char_len_listed = [len(x) for x in text]
    else:
        char_len_listed = len(text)
    return char_len_listed

# GET_TOKEN_COUNT()
# -----------------------------------
# TEXT = str() or list()
# WORDS_PER_PASSAGE/WORD_COUNTER = list() or int(), based on input
# WORDS_LISTED = list(), tokens created with TOKENIZE_TEXT()

def get_token_count(text):
    word_counter = 0
    if isinstance(text, list):
        words_per_passage = []
        words_listed = [tokenize_text(x) for x in text]
        for item in words_listed:
            word_counter = len(item)
            words_per_passage.append(word_counter)
        return words_per_passage, words_listed
    else:
        words_listed = tokenize_text(text)
        word_counter = len(words_listed)
        return word_counter, words_listed

# GET_TOKEN_LEN()
# -----------------------------------
# TOKENS = list() of lists of tokens, output WORDS_LISTED from GET_TOKEN_COUNT() 
# TOKEN_LEN_LST = list(); average token length per item in TEXT

def get_token_len(tokens, token_count):
    token_len_list = []
    for token_list, token_num in zip(tokens, token_count):
        token_len_per_passage = 0
        for token in token_list:
            token_len_per_passage += len(token)
        if token_num != 0:
            token_len_list.append(token_len_per_passage/token_num)
        else:
            token_len_list.append(0)
    return token_len_list

# type-token ratio (TTR) / Ure lexical density, see https://en.wikipedia.org/wiki/Lexical_density#Discussion
# later
"""def get_ttr(text):
    if isinstance(text, list):
        ttr_list = []
        for entry in text:
            entry = re.sub(r'[^\w]', ' ', entry) #remove special chars
            #re.sub('[^A-Za-z0-9 ,.-_\'äöüÄÖÜß]+', '', sample_text)
            entry = entry.lower() # to lower case
            tokens = tokenize_text(entry)
            types = nltk.Counter(tokens)
            ttr_kp = (len(types)/len(tokens)) * 100
            ttr_list.append(ttr_kp)"""

# GET_SENT_LEN()
# -----------------------------------
# TEXT = list(); list of lists or simple list, output from SPLIT_SENTS()
# LISTED_SENT_LEN/AVG_SENT_LEN = list() or int(); average sent length per item in TEXT

def get_sent_len(text):
    listed_sent_len = []
    if any(isinstance(sents_grouped, list) for sents_grouped in text) == True: 
        for sents_grouped in text:
            sent_len_counter = 0
            for sentence in sents_grouped:
                sent_len_counter += len(sentence)
            if len(sents_grouped) != 0:
                avg_sent_len = sent_len_counter / len(sents_grouped)
                listed_sent_len.append(avg_sent_len)
        return listed_sent_len
    else:
        sent_len_counter = 0
        for sent in text:
            sent_len_counter += len(sent) 
        avg_sent_len = sent_len_counter/len(text)
        return avg_sent_len

# -----------------------------------
# CALLING TEXT MEASURES
# -----------------------------------

# prepare statistics dataframe, use inspect to get the input parameters and there values 
# as seen in https://stackoverflow.com/questions/582056/getting-list-of-parameter-names-inside-python-function      
# TO DO: try to use multiple *args here  

# PREPARE_STATS()
# -----------------------------------
# CHAR_LEN, TOKEN_COUNT, TOKEN_LEN, SENT_LEN, CIT_NUM = different text measures created with functions above + citation frequency per passage 
# PREP_STATS = pandas.Dataframe; to prepare data for further analysis

def prepare_stats(char_len, token_count, token_len, sent_len, cit_num):
    frame = inspect.currentframe()
    args, _, _, values = inspect.getargvalues(frame)
    prep_statistics = pd.DataFrame()
    for i in args:
        prep_statistics[str(i)] = pd.Series(values[i])
    return prep_statistics

# SUMMARY_STATS()
# -----------------------------------
# DATAFRAME = pandas.DataFrame 
# SUMSTATS_DF = pandas.Dataframe; summary statistics for DATAFRAME
def summary_stats(dataframe):
    sumstats_df = dataframe.describe()
    return sumstats_df


# GET_STATS()
# -----------------------------------
# TEXT = list(); list of texts (per passage)
# SENTS = list(); list of sents (per passage)
# CIT_NUM = list(); citation frequencies (per passage)
# STATS_DF = pandas.DataFrame; as created with PREPARE_STATS()
# SUMSTATS = pandas.DataFrame; as created with SUMMARY_STATS()

# to easily access prepare_stats() and summary_stats() for multiple texts
def get_stats(text, sents, cit_num):
    char_len = get_char_len(text)
    token_count, tokens = get_token_count(text)
    token_len = get_token_len(tokens, token_count)
    sent_len = get_sent_len(sents)
    stats_df = prepare_stats(char_len, token_count, token_len, sent_len, cit_num)
    sumstats = summary_stats(stats_df)
    return stats_df, sumstats