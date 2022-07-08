# -----------------------------------
# SENTIMENT ANALYSIS
# -----------------------------------

from .processing import tokenize_text

import pandas as pd

from germansentiment import SentimentModel
model = SentimentModel()

# -----------------------------------
# SENTIWS
# -----------------------------------

# SENTIWS_GLOSSARY()
# -----------------------------------
# POSITIVE_LINES = .readlines() output for positive SentiWS file
# POSITIVE_LINES = .readlines() output for negative SentiWS file
# SENTIMENT_GLOSSARY = pandas.DataFrame(); glossary of sentiment values, words etc. to work with
def sentiws_glossary(positive_lines, negative_lines):
    # create df from positive_lines and negative_lines
    sentiment_glossary = pd.DataFrame({'entries':positive_lines})
    sentiment_glossary_neg = pd.DataFrame({'entries':negative_lines})
    sentiment_glossary = sentiment_glossary.append(sentiment_glossary_neg, ignore_index=True)
    # for each entry, split it into corresponding df columns using regex, then delete col "entries"
    sentiment_glossary[['word','pos_tag','polarity','infl']] = sentiment_glossary['entries'].str.extract(r"^(.*)\|(.*)\t(.*)\t(.*)$", expand=True)
    sentiment_glossary = sentiment_glossary.drop(columns="entries")
    # split infl into a list of infls
    infls = [enum_item.split(",") for enum_item in sentiment_glossary.infl]
    sentiment_glossary = sentiment_glossary.drop(columns=["infl"])
    sentiment_glossary["infl"] = infls
    return sentiment_glossary

# GET_POLARITY_VALUES()
# -----------------------------------
# TEXT = list(); subset text
# SENTIMENT_DF = pandas.DataFrame(); sentiment glossary/output of SENTIWS_GLOSSARY()
# SENTIMENT_VALS = list(); all polarity values for TEXT based on SENTIMENT_DF 
def get_polarity_values(text, sentiment_df):
    sentiment_vals = []
    for passage in text:
        passage_val = 0
        tokens = tokenize_text(passage)
        for token in tokens:
            if token in list(sentiment_df.word):
                idx = sentiment_df.index[sentiment_df["word"] == token]
                polarity = sentiment_df.at[idx.values[0], "polarity"]
                passage_val += float(polarity)
            elif any(sentiment_df.infl == token):
                #idx = np.where(sentiment_df["infl"].str.contains(token))
                idx = sentiment_df.index[sentiment_df["infl"].str.contains(token)]
                polarity = sentiment_df.at[idx.values[0], "polarity"]
                passage_val += float(polarity)
        sentiment_vals.append(passage_val)
    return sentiment_vals


# -----------------------------------
# GERMANSENTIMENT
# -----------------------------------

# GET_GERMANSENTIMENT()
# -----------------------------------
# TEXT_COL = pandas.DataFrame.column; text of a specific subset
# SENTIMENT = pandas.DataFrame(); germansentiment value for each text in TEXT_COL
def get_germansentiment(text_col):
    counter = 0
    sentiment = []
    for passage in text_col:
        result = model.predict_sentiment(text_col[counter:counter+1])
        sentiment.append(result)
        counter += 1
    return pd.DataFrame(sentiment, columns=['germansentiment'])

# MAP_SENTIMENT()
# -----------------------------------
# DF = pandas.DataFrame(); must contain column "germansentiment" on which the function is applied
def map_sentiment(df):
    sentiment_mapped = []
    for i in df.germansentiment:
        if i == "neutral":
            sentiment_mapped.append(0)
        elif i == "positive":
            sentiment_mapped.append(1)
        elif i == "negative":
            sentiment_mapped.append(-1)
    df["germansentiment_mapped"] = sentiment_mapped
    return df


# -----------------------------------
# COMPARE SENTIMENT SCORES
# -----------------------------------

# COMPARE_SENTIMENT()
# -----------------------------------
# PASSAGE_LOC = str(); location of passage to inspect
# DF = pandas.DataFrame(); must contain the columns "text", "germansentiment" and "rel_sentiws" for them to be compared
def compare_sentiment(passage_loc, df):
    print("position of passage: " + str(passage_loc))
    print("text: " + df.text[passage_loc])
    print("score using germansentiment: " + str(df.germansentiment[passage_loc]))
    print("score using sentiws: " + str(df.loc[passage_loc, "rel_sentiws"]))