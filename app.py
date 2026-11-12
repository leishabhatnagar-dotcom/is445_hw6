# 1. imports
import streamlit as st
import pandas as pd
import altair as alt


url = "https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv"
cols = ['datetime','city','state','country','shape','duration_seconds',
        'duration_text','comments','date_posted','latitude','longitude']
df = pd.read_csv(url, names=cols, low_memory=False)

filler_words = ["the", "and", "a", "in", "of", "to", "was", "it", "with", "on",
                "at", "i", "my", "we", "for", "then", "from", "that", "were", "is",
                "over", "an", "as", "by", "very", "into", 'saw','seen','object', 'ufo', 
                'shaped',"about", "up", "like", "around", "no", "out", "this", "or", 
                "one", "two", "when", "objects", "sighting","seen", "&#44", "&#39",]
top_shapes =df['shape'].value_counts().head(8).index.tolist()
shape= st.radio("Pick a UFO shape:", top_shapes)
shape_subset = df[df['shape'] == shape]
words = (shape_subset["comments"].dropna().str.lower()
         .str.replace("&#44", " ")
         .str.replace("&#39", "'")
         .str.replace(r"[^a-z\s]", "", regex=True)
         .str.split().explode())
words = words[words.isin(filler_words + [shape,shape+'s']) == False]

counts = words.value_counts().head(10).reset_index()
counts.columns = ['word','count']


chart1 = alt.Chart(counts).mark_bar().encode(
    alt.X('count:Q', title='Number of times used'),
    alt.Y('word:N', sort='-x', title="Word"),
    tooltip=['word','count'],
    color= alt.Color("count:Q", scale=alt.Scale(range=["#f0afd6", "#930045"]),legend=None)
).properties(
    title=f"Most common words in UFO descriptions: {shape}",
    height=500,
    width=350
)

st.altair_chart(chart1)