# -----------------------------------
# FUNCTIONS FOR (PRE-)PROCESSING TEXTS
# -----------------------------------

import nltk
import spacy

#load small german lang model
spacy_ger = spacy.load('de_core_news_sm')

# TOKENIZE_TEXT()
# -----------------------------------
# TEXT = str()
# TOKENS_LISTED = list(); tokens for input text 

def tokenize_text(text):
    tokens_listed = nltk.word_tokenize(text)
    return tokens_listed

# REPLACE_LINEBREAKS()
# -----------------------------------
# TEXT = str()

def replace_linebreaks(text):
    text = text.replace("\n\n", " ").replace("\n", " ")
    return text

# SPLIT_SENTS()
# -----------------------------------
# TEXT = str()
# SENTS_LISTED/SENTENCES = depending on whether the input is a single text file or a list of texts, this function return either a list of sentences or a list of lists of sentences

def split_sents(text):
    if isinstance(text, list):
        sents_listed = []
        for item in text:
            replace_linebreaks(item)
            doc = spacy_ger(item)
            sentences = list(doc.sents)
            sents_listed.append(sentences)
        return sents_listed
    else:
        replace_linebreaks(text)
        doc = spacy_ger(text)
        sentences = list(doc.sents)
        return sentences
        
