#python lib....
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("zomato_cleaned.csv")

st.title("Zomato Bangalore Dashboard")

# Sidebar Filters basics
st.sidebar.header("Filters")
locations = ["All"] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", locations)

if selected_location != "All":
    df = df[df['location'] == selected_location]

# KPI Cards from filterd data 
col1, col2, col3 = st.columns(3)
col1.metric("Total Restaurants", len(df))
col2.metric("Average Rating", round(df['rate'].mean(), 2))
col3.metric("Avg Cost for Two", f"₹{int(df['cost_for_two'].mean())}")


# st.subheader("Restaurant Data")
# st.dataframe(df[['name', 'location', 'rate', 'cost_for_two', 'cuisines']].reset_index(drop=True))


# Charts for visualization
col1, col2 = st.columns(2)

with col1:
    st.subheader("Rating Distribution")
    fig = px.histogram(df, x='rate', nbins=20)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Cuisines")
    top_cuisines = df['cuisines'].value_counts().head(10).reset_index()
    top_cuisines.columns = ['cuisine', 'count']
    fig2 = px.bar(top_cuisines, x='count', y='cuisine', orientation='h')
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Cost vs Rating")
fig3 = px.scatter(df, x='cost_for_two', y='rate', opacity=0.4)
st.plotly_chart(fig3, use_container_width=True)


st.subheader("Restaurant Data")
st.dataframe(df[['name', 'location', 'rate', 'cost_for_two', 'cuisines']].reset_index(drop=True))
