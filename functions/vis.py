# -----------------------------------
# COLLECTION OF VIS FUNCTIONS
# -----------------------------------

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from plotly.subplots import make_subplots

import numpy

# -----------------------------------
# META SETTINGS
# -----------------------------------

color_palette = ["#509F98", "#C16152", "#EDB85C", "#5d73b8", "#9B8945"]
# "#A67D85"
fonts = ["CMU Serif",] # define LaTeX font (Computer Modern) as fonttype for vis 

# WRITE_VIS()
# -----------------------------------
# EXTENSIONS = list(); list of all the extension in which the vis should be saved
# FILENAME = str(); name of file (without extension)
# FIG = figure

def write_vis(extensions, filename, fig):
    for extension in extensions:
        if extension == "html":
            fig.write_html(filename + "." + extension)
        else:
            pio.write_image(fig, filename + "." + extension)

# -----------------------------------
# STATS VIS
# -----------------------------------


# BOX_PLOT()
# -----------------------------------
# DF_COLS = list(), pandas.DataFrame column names
# DF_NAMES = list(); str() names for cols in DF_COLS, used for labelling 
# ATTRIBUTE = str(); attribute (e.g. text stat) to inspect
# FIG = figure

def box_plot(df_cols, df_names, attribute):
    fig = go.Figure()
    counter = 0
    color_counter = 0
    col_names = {}
    col_names_str = ""
    for col in df_cols:
        trace_name = df_names[counter] + " " + col.name
        col_names[counter] = {} # create a nested dict, because keys (df_names) can be identical -> however, it might be better to use a nested dictionary from the start (as function parameter)
        col_names[counter][df_names[counter]] = col.name
        if color_counter < len(color_palette):
            fig.add_trace(go.Box(y=col, name=trace_name, boxpoints="outliers", marker=dict(opacity=0.5, color=color_palette[color_counter]), marker_size=5, ))
        else:
            color_counter = 0
            fig.add_trace(go.Box(y=col, name=trace_name, boxpoints="outliers", marker=dict(opacity=0.5,  color=color_palette[color_counter]), marker_size=5,))
        color_counter += 1
        counter += 1
    print(col_names)
    for key, value in col_names.items():
        for k, v in value.items():
            col_names_str += (k + "_" + v + "-")
    fig.update_layout(template="plotly_dark", font=dict(family = fonts[0]), showlegend=False, xaxis_title="subset", yaxis_title=attribute,)
    fig.show()
    return fig

# SCATTER_PLOT()
# -----------------------------------
# DF = pandas.DataFrame
# DF_NAME = str(), name of DF, used for title text
# COLX = str(); column 1 of DF to inspect
# COLY = str(); column 2 of DF to inspect
# FIG = figure

def scatter_plot(df, df_name, colx, coly):
    fig = px.scatter(df, x=colx, y=coly, opacity=.5)
    fig.update_traces(marker_color=color_palette[0])
    fig.update_layout(title_text="relationship " + colx + " and " + coly + " in " + df_name, template="plotly_dark", font=dict(family = fonts[0]))
    fig.show()
    return fig

# -----------------------------------
# VIS FOR POS
# -----------------------------------

# VIS_SUBPLOTS()
# -----------------------------------
# SUBTITLES = list() of str() for each subtitle
# DATAFRAMES = list() of pandas.DataFrames, here NGRAMS output from GET_N_NGRAMS()
# ROWCOUNT = int(), number of rows for subplot
# COLCOUNT = int(), number of columns for subplot
# SHOWLABELS = binary, show label for each subplot
# REL_YAXIS = binary, if yes all following subplots have the same y axis scale as the first one
# FIG = plotly.graph_objects.Figure

# subplots, used here for different ngram counts
def vis_subplots(subtitles, dataframes, rowcount, colcount, showlabels, rel_yaxis):
    if (rowcount * colcount < len(subtitles)) or (rowcount * colcount > len(subtitles)):
      print("The sum of rows and cols does not fit the number of assigned dataframes. Data might be lost.")
    fig = make_subplots(
    rows=rowcount, cols=colcount,
    subplot_titles=subtitles,)
    # counters to iterate through cols and rows until colcount is reached, then next row
    col_counter = 0 
    row_counter = 1
    color_counter = 0
    for df in dataframes:
        if color_counter < len(color_palette):
            fig.add_trace(go.Bar(x=df["ngram"], y=df["count"], marker=dict(color=color_palette[color_counter]),),
              row=row_counter, col=col_counter+1)
        else:
            color_counter = 0
            fig.add_trace(go.Bar(x=df["ngram"], y=df["count"], marker=dict(color=color_palette[color_counter]),),
              row=row_counter, col=col_counter+1)
        color_counter += 1
        col_counter += 1
        if (col_counter == colcount) & (row_counter < rowcount):
          row_counter += 1
          col_counter = 0
    fig.update_layout(template="plotly_dark", showlegend=False, font=dict(family = fonts[0]))
    # to make subplots comparable in their yaxes value, set rel_yaxis == True
    if rel_yaxis == True:
      fig.update_yaxes(range=[0,dataframes[0].iloc[0]["count"]]) 
    # to show labels, set showlabels == True
    # however, there is some overlapping with very long labels
    if showlabels == True:
        fig.update_xaxes(automargin=True)
    else:
        fig.update_xaxes(visible=False, showticklabels=False)
    return fig

# CALCULATE_WEIGHTS()
# -----------------------------------
# DF (input) = pandas.DataFrame; equals SORTED_TAG_FREQS from COUNT_TAG_FREQS()
# CIT_NUM = list(); citation frequencies per passage
# DF (output) = pandas.DataFrame; equals DF (input) but with newly calculated values 

# first, add functions to calculate weights here
# could be integrated into POS_HEATMAP() as an option as well
def calculate_weights(df, cit_num):
    for (f, b) in zip(df.columns, cit_num):
        for tag in df[f]:
            if numpy.isnan(tag):
                pass
            else:
                weighted_val = round(tag*b)
                df = df.replace(to_replace=tag, value=weighted_val)
    return df

# POS_HEATMAP()
# -----------------------------------
# DF = pandas.DataFrame
# FIG = plotly.graph_objects.Figure

# vis heatmap, weighted as condition
def pos_heatmap(df):
    fig = go.Figure(data=go.Heatmap(
                    x=df.columns, y=df.index, z=df, colorscale=[color_palette[0], color_palette[1]]))
    fig.update_yaxes(categoryorder='category descending')
    fig.update_layout(template="plotly_dark", yaxis=dict(title="POS tag"), xaxis=dict(title="position of passage (chronological order)"),font=dict(family = fonts[0]))
    return fig
