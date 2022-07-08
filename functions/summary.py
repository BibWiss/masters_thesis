# -----------------------------------
# SUMMARY
# -----------------------------------

from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler

# APPLY_SCALING()
# -----------------------------------
# DATAFRAME (INPUT) = pandas.DataFrame
# COL = column in pandas.DataFrame that apply_scaling should be applied to
# SCALE_RANGE = (currently) one of two options: "zero_pos" equals range[0, 1], "neg_pos" equals range[-1, 1]
# DATAFRAME (OUTPUT) = pandas.DataFrame
def apply_scaling(dataframe, col, scale_range):
    if scale_range == "zero_pos":
        X = dataframe[col].to_numpy()
        X = X.reshape(-1, 1)
        transformer = MinMaxScaler().fit(X)
        dataframe.drop(columns=[col])
        new_col = transformer.transform(X)
        dataframe[col] = new_col
    elif scale_range == "neg_pos":
        X = dataframe[col].to_numpy()
        X = X.reshape(-1, 1)
        transformer = MaxAbsScaler().fit(X)
        dataframe.drop(columns=[col])
        new_col = transformer.transform(X)
        dataframe[col] = new_col
    return dataframe