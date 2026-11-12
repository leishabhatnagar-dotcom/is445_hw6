# 1. imports
import streamlit as st
import pandas as pd
import altair as alt


url = "https://github.com/UIUC-iSchool-DataViz/is445_data/raw/main/ufo-scrubbed-geocoded-time-standardized-00.csv"
cols = ['datetime','city','state','country','shape','duration_seconds',
        'duration_text','comments','date_posted','latitude','longitude']
df = pd.read_csv(url, names=cols, low_memory=False)
df['datetime'] = pd.to_datetime(df['datetime'])
alt.data_transformers.disable_max_rows()
df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['hour'] = df['datetime'].dt.hour

filler_words = ["the", "and", "a", "in", "of", "to", "was", "it", "with", "on",
                "at", "i", "my", "we", "for", "then", "from", "that", "were", "is",
                "over", "an", "as", "by", "very", "into", 'saw','seen','object', 'ufo', 
                'shaped',"about", "up", "like", "around", "no", "out", "this", "or", 
                "one", "two", "when", "objects", "sighting","seen", 'other','unknown', 'sky'"&#44", "&#39",]
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

st.markdown("""
This bar chart shows the top 10 most common words for each of the top 8 most common shapes. 
I found that light, bright, and sky were the most common descriptors, followed closely by orange and flying.
I chose the bar chart as it was the clearest method to display the difference in counts of each word. 
Regarding encoding types, I chose quantitative for the count, as it numerically counts how many times each word appears, 
and since every word is equally important, the word’s encoding type was nominal, a category with no order.
I sorted the bars from most to least common so the top words stand out, and 
used a color gradient from light to dark pink to emphasize that further.
When making this chart, I had an initial list of filler words I deemed unimportant to the chart, and then, 
after testing to see which words were the most common, I removed other words that had no impact on the description,
such as “object” or the name of the shape itself. To clean the data, I removed all punctuation and numbers, 
made everything lowercase, and then exploded each word onto its own row. 
Finally, to switch between shapes, I used the radio buttons from the class example so people can click on 
different shapes to see how they compare. To improve this visualization,
I would look more thoroughly and remove more generic words, or add a second variable to find a trend.

""")


chart2 = alt.Chart(df[['month','hour']]).mark_rect().encode(
    alt.X('hour:O', title="Hour of day (0=midnight)"),
    alt.Y('month:O', title="Month"),
    alt.Color("count()", 
              scale=alt.Scale(range=["#f7d7ea", "#930045"]), 
              title="Number of Sightings")
).properties(
    title= "UFO Sightings Heatmap by Calendar Year",
    height=300,
    width=600
)
st.altair_chart(chart2, theme=None, use_container_width=True)
st.markdown("""
This next chart organizes UFO sightings by month and hour of day, across all shapes. 
I noticed that sightings peak in the evening, and the darkest square is July around 9–10pm, 
which could be due to July 4th fireworks or just general summer nights. Likewise, 
daytime is consistently pale throughout the year. I chose a heatmap made of rectangles 
because it can show two variables at once and is the easiest way to display hot spots or gradual trends. 
I kept the color gradient the same to match chart 1, where the darker the rectangle the more sightings. 
I encoded hour and month as ordinal categories, since their order matters, and I used Altair’s 
built-in count() function, which is quantitative. To simplify the data,
I only passed in the month and hour columns, which came from my data cleaning. 
I also added axis labels and a legend to make the graph easier to read. 
I used similar data cleaning to what I did in HW5. With more time, I would add month names, 
and possibly another radio button or variable to see what trends emerge. 
""")