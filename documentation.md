# Documentation

## 📥 Step 0: Extraction

### [extract_passages.py](0_extraction/extract_passages.py)

#### Description

A small program to extract key passage texts based on their (start/end)
position in the text. Inputs are defined as a literary text and the corresponding citation_sources file, created with [Lotte](https://scm.cms.hu-berlin.de/schluesselstellen/lotte). Returns a <code>.csv</code> file or a <code>.pkl</code> file containing the texts of all cited passages and additional information. For now, this script only works if called from the <code>lotte-develop</code> repo, might need to be rewritten for other purposes.

#### Usage

<code>extract_passages.py [-h] [-o {.csv,.pkl}] -c {.json} -t {.txt}</code>

**required named arguments:**
* <code>-c</code>, <code>--citations</code>: citation_sources path/file name (file type:  <code>{.json}</code>)
* <code>-t</code>, <code>--text</code>: literary text path/file name (file type:  <code>{.txt}</code>)

**optional arguments:**
* <code>-h</code>, <code>--help</Code>: show this help message and exit
* <code>-o</code>, <code>--output</code>: output path / file name (file type:  <code>{.csv,.pkl}</code>)

### [group_passages.py](0_extraction/group_passages.py)

#### Description

This Python script allows us to divide our literary text into two groups - one consisting of potential key passages ("cited") and one containing the rest ("not cited"). A <code>.pkl</code> file created with <code>extract_passages.py</code> is needed as input and another <code>.pkl</code> file containing all text passages is returned.

#### Usage

<code>group_passages.py [-h] [-w WORK] -i {.pkl} -t {.txt}</code>

**required named arguments:**
* <code>-i</code>, <code>--input</code>: input path/file name (file type: <code>{.pkl}</code>)
* <code>-t</code>, <code>--text</code>: literary text path/file name (file type: <code>{.txt}</code>)

**optional arguments:**
* <code>-h</code>, <code>--help</code>: show this help message and exit
* <code>-w</code> , <code>--work</code>:  title of the work, used for output file names (type: <code>{str([WORK])}</code>)#

## 📄 Step 1: Textual Statistics

* **Prerequisites:** <code>j_all.pkl</code> and <code>k_all.pkl</code>, as created in Step 0 with <code>group_passages.py</code> (here: [data/0_extraction_data](data/0_extraction_data))
* **Output:** [data/1_text-stats_data](data/1_text-stats_data)

### Notebook
* path: [1_text-stats.ipynb](1_text-stats.ipynb)
* libraries that need to be installed:
    * [plotly](https://plotly.com/python/)
    * [scipy](https://scipy.org/)
    * [pandas](https://pandas.pydata.org/)
    * [spacy](https://spacy.io/)
    * [nltk](https://www.nltk.org/)

### Functions  
* Python scripts used: [basic.py](functions/basic.py), [processing.py](functions/processing.py), [stats.py](functions/stats.py), [vis.py](functions/vis.py)

#### Preparation

**<code>text/df = read_file(filepath)</code>**<br><a name="read_file"></a>
Reads a <code>.txt</code> or a <code>.pkl</code> file.

| name      | description |
| ----------- | ----------- |
| <code>filepath</code>      | name of the file/filepath <br> **type:** <code>str</code>     |
| <code>text/df</code>     | file content, based on <code>filepath</code>  it is either a <ul><li>**type:** <code>str</code> or</li><li>**type:** <code>pandas.DataFrame</code></li></ul>       |

**<code>sents_listed/sentences = split_sentences(text)</code>**<br><a name="split_sents"></a>
Splits an input <code>text</code> into sentences.

| name      | description |
| ----------- | ----------- |
| <code>text</code>      | **type:** <code>str</code> or <code>list</code>    |
| <code>sents_listed/sentences</code>     | depending on whether the input is a single text file or a list of texts, this function return either a <ul><li><code>list</code> of sentences or</li><li><code>list</code> of <code>lists</code> of sentences or</li><li>**type:** <code>list</code></li></ul>       |

#### Textual Statistics

**<code>stats_df, sumstats = get_stats(text, sents, cit_num)</code>**<br><a name="get_stats"></a>
Returns a <code>pandas.DataFrame</code> of text statistics (character length, token count, token length and sentence length per passage) as well as a <code>pandas.DataFrame</code> with the corresponding summary statistics. For functions <code>prepare_stats()</code> and  <code>summary_stats()</code> as well as the calculation of the different text statistics ( <code>get_char_len()</code>,  <code>get_token_count()</code>,  <code>get_token_len()</code>,  <code>get_sent_len()</code>), please take a look at [stats.py](functions/stats.py).

| name      | description |
| ----------- | ----------- |
| <code>text</code>      | list of texts (per passage) <br> **type:** <code>list</code>    |
| <code>sents</code>      | list of sentences (per passage) <br> **type:** <code>list</code>    |
| <code>cit_num</code>      | list of citation frequencies (per passage) <br> **type:** <code>list</code>    |
| <code>stats_df</code>     | output  from <code>prepare_stats()</code> <br> **type:** <code>pandas.DataFrame</code>    |
| <code>sumstats</code>     | output from <code>summary_stats()</code> <br> **type:** <code>pandas.DataFrame</code>       |

#### Vis

**<code>fig = box_plot(df_cols, df_names, attribute)</code>**<br><a name="box_plot"></a>
Returns a box plot for the given columns and attribute.
| name      | description |
| ----------- | ----------- |
| <code>df_cols</code>      | <code>pandas.DataFrame</code> column names to compare <br> **type:** <code>list</code>    |
| <code>df_names</code>      | <code>str</code> names for columns in <code>df_cols</code>, used for labelling purposes <br> **type:** <code>list</code>    |
| <code>attribute</code>      | attribute (e.g. textual statistic) to inspect <br> **type:** <code>str</code>  |
| <code>fig</code>     |figure <br> **type:**  <code>plotly.graph_objects.Figure</code>  |

**<code>fig = scatter_plot(df, df_name, colx, coly)</code>**<br><a name="scatter_plot"></a>
Returns a scatter plot for the given columns in <code>df</code>.
| name      | description |
| ----------- | ----------- |
| <code>df</code>      | **type:** <code>pandas.DataFrame</code>   |
| <code>df_name</code>      | name of <code>df</code> , used for title text <br> **type:** <code>str</code>    |
| <code>colx</code>      | column 1 of DF to inspect <br> **type:** <code>str</code>  |
| <code>coly</code>      | column 1 of DF to inspect <br> **type:** <code>str</code>  |
| <code>fig</code>     |figure <br> **type:**  <code>plotly.express.scatter</code> |

## 🏷 Step 2: Part-of-Speech (POS) Tagging

* **Prerequisites:** all files in [data/1_text-stats_data](data/1_text-stats_data)
* **Output:** [data/2_pos_data](data/2_pos_data)

### Notebook
* path: [2_pos.ipynb](2_pos.ipynb)
* libraries that need to be installed:
    * [plotly](https://plotly.com/python/)
    * [pandas](https://pandas.pydata.org/)
    * [spacy](https://spacy.io/)
    * [numpy](https://numpy.org/)
    * [statsmodels](https://www.statsmodels.org/stable/index.html)

### Functions  
* Python scripts used: [basic.py](functions/basic.py), [processing.py](functions/processing.py), [pos.py](functions/pos.py), [vis.py](functions/vis.py)

#### Preparation

[<code>read_file()</code>](#read_file)

[<code>split_sents()</code>](#split_sents)

#### (Relative) Frequencies

**<code>pos_tagged_dict, pos_tagged_list = get_pos_tags(sents)</code>**<br><a name="get_pos_tags"></a>
Returns a <code>dict</code> and <code>list</code> of POS Tags for all of the passages.
| name      | description |
| ----------- | ----------- |
| <code>sents</code>      | list of lists of sentences, as created using <code>split_sents()</code> <br> **type:** <code>list</code>   |
| <code>pos_tagged_dict</code>      | all individual terms (= each term once per passage) and their associated POS Tags <br> **type:** <code>dict</code>    |
| <code>pos_tagged_list</code>      | all POS Tags per passage in their original order <br> **type:** <code>list</code>  |

**<code>sorted_tag_freqs, tags_used = count_tag_freqs(pos_tagged)</code>**<br><a name="count_tag_freqs"></a>
Counts the individual POS Tag frequencies per passage in <code>pos_tagged</code>.
| name      | description |
| ----------- | ----------- |
| <code>pos_tagged</code>      |output <code>pos_tagged_list</code> from [<code>get_pos_tags</code>](#get_pos_tags) <br> **type:** <code>list</code>   |
| <code>sorted_tag_freqs</code>      | DataFrame where row = tag name, column = index of passage, values = relative frequencies <br> **type:** <code>pandas.DataFrame</code>    |
| <code>tags_used</code>      | all individual POS Tags used within an input text/document <br> **type:** <code>list</code>  |

**<code>fig = pos_heatmap(df)</code>**<br><a name="pos_heatmap"></a>
Returns a heatmap visualization for the input <code>df</code>.
| name      | description |
| ----------- | ----------- |
| <code>df</code>      |output <code>sorted_tag_freqs</code> from [<code>count_tag_freqs</code>](#count_tag_freqs) <br> **type:** <code>pandas.DataFrame</code>   |
| <code>fig</code>      | figure <br> **type:** <code>plotly.graph_objects.Figure</code>    |

**<code>df = calculate_weights(df, cit_num)</code>**<br><a name="calculate_weights"></a>
Calculate weighted values for <code>sorted_tag_freqs</code>.
| name      | description |
| ----------- | ----------- |
| <code>df (input)</code>      |output <code>sorted_tag_freqs</code> from [<code>count_tag_freqs</code>](#count_tag_freqs) <br> **type:** <code>pandas.DataFrame</code>   |
| <code>cit_num</code>      | citation frequencies per passage <br> **type:** <code>list</code>    |
| <code>df (output)</code>      | equals <code>df (input)</code> but with newly calculated values  <br> **type:** <code>pandas.DataFrame</code>    |

#### n-grams

**<code>ngrams_list = find_ngrams(pos_tagged, n)</code>**<br><a name="find_ngrams"></a>
Return a list of <code>n</code>-Grams for <code>pos_tagged</code>.
| name      | description |
| ----------- | ----------- |
| <code>pos_tagged</code>      |output <code>pos_tagged</code> from [<code>get_pos_tags</code>](#get_pos_tags) <br> **type:** <code>list</code>   |
| <code>n</code>      | n as in n-Gram <br> **type:** <code>int</code>    |
| <code>ngrams_list</code>      | all the corresponding n-Grams found  <br> **type:** <code>list</code>    |

**<code>df = ngram_count(ngrams)</code>**<br><a name="ngram_count"></a>
Counts the frequencies of each ngram in <code>ngrams</code> and returns them as a <code>pandas.DataFrame</code>.
| name      | description |
| ----------- | ----------- |
| <code>ngrams</code>      |output <code>ngrams_list</code> from [<code>find_ngrams</code>](#find_ngrams) <br> **type:** <code>list</code>   |
| <code>df</code>      | DataFrame containing the columns "ngram" and "count" <br> **type:** <code>pandas.DataFrame</code>    |

**<code>ngrams, names = get_n_ngrams(n, topn, pos_tagged)</code>**<br><a name="get_n_ngrams"></a>
Allows to call [<code>find_ngrams</code>](#find_ngrams) and [<code>ngram_count</code>](#ngram_count) for more than one <code>n</code> and limit results to a <code>topn</code> count.
| name      | description |
| ----------- | ----------- |
| <code>n</code>      |<code>list</code> of <code>int</code>s, n as in n-Gram <br> **type:** <code>list([int_1, int_2, int_n])</code>   |
| <code>top</code>      | describes how many highest values to return <br> **type:** <code>int</code>    |
| <code>pos_tagged</code>      | output <code>pos_tagged</code> from [<code>get_pos_tags</code>](#get_pos_tags) <br> **type:** <code>list</code>   |
| <code>ngrams</code>      | returns a <code>pandas.DataFrame</code> similar to output <code>df</code> from [<code>ngram_count</code>](#ngram_count) for each <code>n</code>  <br> **type:** <code>list</code>    |
| <code>names</code>      | contains names for each of the nested <code>pandas.DataFrames</code> in <code>ngrams</code> to use for visualization purposes  <br> **type:** <code>list</code>    |

**<code>fig = vis_subplots(subtitles, dataframes, rowcount, colcount, showlabels, rel_yaxis)</code>**<br><a name="vis_subplots"></a>
Create a <code>plotly.graph_objects.Fig</code> consisting of several bar subplots for each DataFrame in <code>dataframes</code>.
| name      | description |
| ----------- | ----------- |
| <code>subtitles</code>      |<code>list</code> of <code>str</code>s for each subtitle <br> **type:** <code>list</code>   |
| <code>dataframes</code>      | <code>list</code> of <code>pandas.DataFrame</code>s, output <code>ngrams</code> from [<code>get_n_grams</code>](#get_n_grams) <br> **type:** <code>list</code>    |
| <code>rowcount</code>      | number of rows for subplots <br> **type:** <code>int</code>   |
| <code>colcount</code>      | number of columns for subplots <br> **type:** <code>int</code>   |
| <code>showlabels</code>      | whether to show labels for subplots or not  <br> **type:** <code>binary</code>    |
| <code>rel_yaxis</code>      | if <code>True</code> all following subplots have the same y-axis scale as the first one  <br> **type:** <code>binary</code>    |
| <code>fig</code>      | **type:** <code>plotly.graph_objects.Fig</code>    |

**<code>all_grams_list = list_individual_grams(df_lists)</code>**<br><a name="list_individual_grams"></a>
Return all individual n-grams over all input <code>df_lists</code>.
| name      | description |
| ----------- | ----------- |
| <code>df_lists</code>      |<code>list</code> of <code>pandas.DataFrame</code>s that equal the output <code>ngrams</code> from [<code>get_n_grams</code>](#get_n_ngrams) <br> **type:** <code>list</code>   |
| <code>all_grams_lists</code>      |  all individual ngrams over the different input DataFrames in <code>df_lists</code> <br> **type:** <code>list</code>    |

**<code>check_grams = grams_matrix_prep(grams, all_grams, type)</code>**<br><a name="grams_matrix_prep"></a>
Checks for each n-gram in <code>grams</code> whether it occurs or not (<code>"binary"</code>) or how often it occurs (<code>"count"</code>), depending on <code>type</code>. Returns a <code>list</code> of values.
| name      | description |
| ----------- | ----------- |
| <code>grams</code>      | equals output <code>ngrams</code> from [<code>get_n_grams</code>](#get_n_ngrams) <br> **type:** <code>pandas.DataFrame</code>   |
| <code>all_grams</code>      |  output <code>all_grams_list</code> from [<code>list_individual_grams</code>](#list_individual_grams) <br> **type:** <code>list</code>    |
| <code>type</code>      | options are <code>"binary"</code> and <code>"count"</code>, does not (spell-)check them right now <br> **type:** <code>str</code>   |
| <code>check_grams</code>      |  returns a <code>list</code> of binary/count values for each n-gram in <code>all_grams</code> <br> **type:** <code>list</code>    |

**<code>index_list = find_ngram_index(pos_tagged, ngram)</code>**<br><a name="find_ngram_index"></a>
Finds all indices of passages in <code>pos_tagged</code> that contain a certain <code>ngram</code> at least once.
| name      | description |
| ----------- | ----------- |
| <code>pos_tagged</code>      | output <code>pos_tagged_list</code> from [<code>get_pos_tags</code>](#get_pos_tags) <br> **type:** <code>list</code>   |
| <code>ngram</code>      |  must be in the following format (use <code>,</code> as delimiter): <code>"[pos_tag],[pos_tag_2],[pos_tag_n]"</code><br> **type:** <code>str</code>    |
| <code>index_list</code>      | **type:** <code>list</code>   |

#### Diversity

**<code>div_df = get_pos_diversity(df)</code>**<br><a name="get_pos_diversity"></a>
Calculate Shannon Entropy for all POS Tag frequencies per passage in <code>df</code> and returns them in a <code>pandas.DataFrame</code>.
| name      | description |
| ----------- | ----------- |
| <code>df</code>      | output <code>sorted_tag_freqs</code> from [<code>count_tag_freqs</code>](#count_tag_freqs) <br> **type:** <code>pandas.DataFrame</code>   |
| <code>div_df</code>      |  DataFrame containing the column "pos_diversity" <br> **type:** <code>pandas.DataFrame</code>    |

## 🙃 Step 3: Sentiment Analysis

* **Prerequisites:** all files in [data/2_pos_data](data/2_pos_data)
* **Output:** [data/3_sentiment_data](data/3_sentiment_data)

### Notebook
* path: [3_sentiment.ipynb](3_sentiment.ipynb)
* libraries that need to be installed:
    * [plotly](https://plotly.com/python/)
    * [pandas](https://pandas.pydata.org/)
    * [spacy](https://spacy.io/)
    * [nltk](https://www.nltk.org/)
    * [germansentiment](https://huggingface.co/oliverguhr/german-sentiment-bert)
    * [sklearn](https://scikit-learn.org/stable/)

### Functions  
* Python scripts used: [basic.py](functions/basic.py), [processing.py](functions/processing.py), [sentiment.py](functions/sentiment.py), [summary.py](functions/summary.py)

#### Preparation 
[<code>read_file()</code>](#read_file)

[<code>split_sents()</code>](#split_sents)

#### SentiWS 
**<code>sentiment_glossary = sentiws_glossary(positive_lines, negative_lines)</code>**<br><a name="sentiws_glossary"></a>
Return all [SentiWS](https://wortschatz.uni-leipzig.de/de/download) data in form of a <code>pandas.DataFrame</code>.
| name      | description |
| ----------- | ----------- |
| <code>positive_lines</code>      | file <code>SentiWS_v2.0_Positive.txt</code>, read with <code>.readlines()</code> <br> **type:** <code>list</code>   |
| <code>negative_lines</code>      | file <code>SentiWS_v2.0_Negative.txt</code>, read with <code>.readlines()</code> <br> **type:** <code>list</code>   |
| <code>sentiment_glossary</code>      | processable glossary of words and their sentiment values to work with <br> **type:** <code>pandas.DataFrame</code>    |

**<code>sentiment_vals = get_polarity_values(text, sentiment_df)</code>**<br><a name="get_polarity_values"></a>
Return a sentiment value for each passage in <code>text</code>.
| name      | description |
| ----------- | ----------- |
| <code>text</code>      | **type:** <code>list</code>   |
| <code>sentiment_df</code>      | output <code>sentiment_glossary</code> from [<code>sentiws_glossary</code>](#sentiws_glossary) <br> **type:** <code>pandas.DataFrame</code>   |
| <code>sentiment_vals</code>      | all polarity values for <code>text</code> based on <code>sentiment_df</code> <br> **type:** <code>list</code>    |

**<code>dataframe = apply_scaling(dataframe, col, scale_range)</code>**<br><a name="apply_scaling"></a>
Apply a new scale to all data in one <code>col</code> of <code>dataframe (input)</code>.
| name      | description |
| ----------- | ----------- |
| <code>dataframe (input)</code>      | **type:** <code>pandas.DataFrame</code>   |
| <code>col</code>      |  column in <code>dataframe (input)</code> that <code>apply_scaling</code> should be applied to <br> **type:** <code>str</code>   |
| <code>scale_range</code>      | (currently) one of two options: <code>"zero_pos"</code> equals range [0, 1] (using <code>sklearn.preprocessing.MinMaxScaler</code>), <code>"neg_pos"</code> equals range [-1, 1] (using <code>sklearn.preprocessing.MaxAbsScaler</code>) <br> **type:** <code>str</code>    |
| <code>dataframe (output)</code>      | **type:** <code>pandas.DataFrame</code>   |

#### germansentiment 

**<code>sentiment = get_germansentiment(text_col)</code>**<br><a name="get_germansentiment"></a>
Calculate sentiment_scores for each passage in <code>text_col</code> and return a DataFrame.
| name      | description |
| ----------- | ----------- |
| <code>text_col</code>      | **type:** <code>pandas.DataFrame[column]</code>   |
| <code>sentiment</code>      |  <code>germansentiment.SentimentModel().predict_sentiment()</code> for each text in <code>text_col</code> <br> **type:** <code>pandas.DataFrame</code>   |

**<code>compare_sentiment(passage_loc, df)</code>**<br><a name="compare_sentiment"></a>
Prints out germansentiment and SentiWS Scores for a given <code>passage_loc</code> in <code>df</code>.

| name      | description |
| ----------- | ----------- |
| <code>passage_loc</code>      | location (index) of passage to inspect <br> **type:** <code>int</code>   |
| <code>df</code>      |  must contain the columns <code>"text"</code>, <code>"germansentiment"</code> and <code>"rel_sentiws"</code> for them to be compared <br> **type:** <code>pandas.DataFrame</code>   |

**<code>df = map_sentiment(df)</code>**<br><a name="map_sentiment"></a>
Transforms germansentiment values in <code>df</code> to a [-1, 0, 1] scale.

| name      | description |
| ----------- | ----------- |
| <code>df (input/output)</code>      |  must contain the column <code>"germansentiment"</code> on which the function is applied <br> **type:** <code>pandas.DataFrame</code>   |

## 🗂 Step 4: Summary

* **Prerequisites:** all files in [data/3_sentiment_data](data/3_sentiment_data)
* **Output:** [data/4_summary_data](data/4_summary_data)

### Notebook
* path: [4_summary.ipynb](4_summary.ipynb)
* libraries that need to be installed:
    * [pandas](https://pandas.pydata.org/)
    * [sklearn](https://scikit-learn.org/stable/)
    * [matplotlib](https://matplotlib.org/stable/)

### Functions  

[<code>read_file()</code>](#read_file)

[<code>apply_scaling()</code>](#apply_scaling)