import numpy as np
import pandas as pd
import networkx as nx
import operator

headers = ['video_ID', 'uploader', 'age', 'category', 'length', 'views', 'rate', 'ratings', 
           'comments', "related_ID_0", "related_ID_1", "related_ID_2", "related_ID_3", 
           "related_ID_4", "related_ID_5", "related_ID_6", "related_ID_7", "related_ID_8", 
           "related_ID_9", "related_ID_10", "related_ID_11", "related_ID_12", "related_ID_13", 
           "related_ID_14", "related_ID_15", "related_ID_16", "related_ID_17", "related_ID_18", "related_ID_19"]

def sanitize(col):
    return col.str.strip()

def combine_related(col):
    return col.dropna().astype(str).values.tolist()

def process_file(filename):
    df = pd.read_csv(filename, sep='\t', header=None, names=headers, engine='python', error_bad_lines=False)

    if len(df.columns) < 29:
        raise Exception('Too few columns in file {0}'.format(filename))

    # combine the last 20 columns into a single one
    related = df.iloc[:,9:]
    dfmain = df.iloc[:,:9]
    
    strings = dfmain.select_dtypes(include='object').apply(axis=1, func=sanitize)
    numbers = dfmain.select_dtypes(include='number')

    df = pd.concat([strings, numbers], axis=1)
    df["related_IDs"]= related.apply(axis=1, func=combine_related)
    df['category'] = df['category'].astype('category')

    return df

def process_files(files):
    df = pd.DataFrame()

    for f in files:
        df = pd.concat([df, process_file(f)], axis=0)
    return df

def toEdgelist(dataframe):
    el = dataframe[['video_ID', 'related_IDs']]
    df = el['related_IDs'].apply(lambda x: pd.Series(x)).stack()    \
        .reset_index(level=1, drop=True).to_frame('related_ID')     \
        .join(el[['video_ID']], how='left')
    df.columns = ['dst', 'src']
    return df


# df = process_files(['./data/080609/0.txt', './data/080609/1.txt', './data/080609/2.txt', './data/080609/3.txt'])
# half = toEdgelist(df)
# half.to_pickle('full_df.pkl')

df2 = process_files(['./data/080609/0.txt', './data/080609/1.txt', './data/080609/2.txt'])
half2 = toEdgelist(df2)
half2.to_pickle('half_df.pkl')
# graph2 = nx.from_pandas_edgelist(half2, source='src', target='dst')

# df3 = process_files(['./data/080609/0.txt'])
# half3 = toEdgelist(df3)
# half3.to_pickle('small_df.pkl')
# graph3 = nx.from_pandas_edgelist(half3, source='src', target='dst')

# df2 = process_files([path+'/youtube-video-0.txt', path+'/youtube-video-1.txt', path+'/youtube-video-2.txt'])
# df3 = process_files([path+'/youtube-video-0.txt', path+'/youtube-video-1.txt'])