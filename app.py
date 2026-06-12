import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("zomato_cleaned.csv")
st.title("Zomato Bangalore Dashboard")

# Sidebar Filters
st.sidebar.header("Filters")

locations = ["All"] + sorted(df['location'].unique().tolist())
selected_location = st.sidebar.selectbox("Select Location", locations)

# Cost range filter
min_cost = int(df['cost_for_two'].min())
max_cost = int(df['cost_for_two'].max())
cost_range = st.sidebar.slider(
    "Cost for Two (₹)",
    min_value=min_cost,
    max_value=max_cost,
    value=(min_cost, max_cost),
    step=50
)

# Apply filters
filtered_df = df.copy()
if selected_location != "All":
    filtered_df = filtered_df[filtered_df['location'] == selected_location]
filtered_df = filtered_df[
    (filtered_df['cost_for_two'] >= cost_range[0]) &
    (filtered_df['cost_for_two'] <= cost_range[1])
]

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Restaurants", len(filtered_df))
col2.metric("Average Rating", round(filtered_df['rate'].mean(), 2))
col3.metric("Avg Cost for Two", f"₹{int(filtered_df['cost_for_two'].mean())}")

st.divider()

# --- Row 1: Rating Distribution + Top 10 Cuisines ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Rating Distribution")
    fig = px.histogram(filtered_df, x='rate', nbins=20,
                       color_discrete_sequence=['#fc5a03'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top 10 Cuisines")
    top_cuisines = filtered_df['cuisines'].value_counts().head(10).reset_index()
    top_cuisines.columns = ['cuisine', 'count']
    fig2 = px.bar(top_cuisines, x='count', y='cuisine', orientation='h',
                  color_discrete_sequence=['#fc5a03'])
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# --- Row 2: Online Order + Table Booking pie charts ---
st.subheader("Online Order & Table Booking Breakdown")
col1, col2 = st.columns(2)

with col1:
    online_counts = filtered_df['online_order'].value_counts().reset_index()
    online_counts.columns = ['Online Order', 'Count']
    fig_online = px.pie(online_counts, names='Online Order', values='Count',
                        title="Online Order",
                        color_discrete_sequence=['#fc5a03', '#ffd6c0'])
    st.plotly_chart(fig_online, use_container_width=True)

with col2:
    booking_counts = filtered_df['book_table'].value_counts().reset_index()
    booking_counts.columns = ['Table Booking', 'Count']
    fig_booking = px.pie(booking_counts, names='Table Booking', values='Count',
                         title="Table Booking",
                         color_discrete_sequence=['#fc5a03', '#ffd6c0'])
    st.plotly_chart(fig_booking, use_container_width=True)

st.divider()

# --- Row 3: Top 10 Locations + Restaurant Type ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Locations by Restaurant Count")
    top_locations = filtered_df['location'].value_counts().head(10).reset_index()
    top_locations.columns = ['location', 'count']
    fig_loc = px.bar(top_locations, x='count', y='location', orientation='h',
                     color_discrete_sequence=['#fc5a03'])
    fig_loc.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_loc, use_container_width=True)

with col2:
    st.subheader("Restaurant Type Distribution")
    rest_types = filtered_df['rest_type'].value_counts().head(10).reset_index()
    rest_types.columns = ['type', 'count']
    fig_type = px.bar(rest_types, x='count', y='type', orientation='h',
                      color_discrete_sequence=['#fc5a03'])
    fig_type.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_type, use_container_width=True)

st.divider()

# --- Budget Analysis ---
st.subheader("Budget Analysis")
budget_bins = [0, 200, 500, 1000, 2000, 99999]
budget_labels = ['Under ₹200', '₹200–500', '₹500–1000', '₹1000–2000', 'Above ₹2000']
filtered_df['budget_category'] = pd.cut(
    filtered_df['cost_for_two'],
    bins=budget_bins,
    labels=budget_labels
)
budget_dist = filtered_df['budget_category'].value_counts().reset_index()
budget_dist.columns = ['Budget Range', 'Count']
budget_dist = budget_dist.sort_values('Budget Range')

col1, col2 = st.columns(2)
with col1:
    fig_budget = px.bar(budget_dist, x='Budget Range', y='Count',
                        color_discrete_sequence=['#fc5a03'])
    st.plotly_chart(fig_budget, use_container_width=True)

with col2:
    # Avg rating per budget category
    avg_rating_budget = filtered_df.groupby('budget_category', observed=True)['rate'].mean().reset_index()
    avg_rating_budget.columns = ['Budget Range', 'Avg Rating']
    fig_br = px.bar(avg_rating_budget, x='Budget Range', y='Avg Rating',
                    color_discrete_sequence=['#fc5a03'],
                    title="Avg Rating by Budget")
    fig_br.update_yaxes(range=[0, 5])
    st.plotly_chart(fig_br, use_container_width=True)

st.divider()

# --- Cost vs Rating scatter ---
st.subheader("Cost vs Rating")
fig3 = px.scatter(filtered_df, x='cost_for_two', y='rate', opacity=0.4,
                  color_discrete_sequence=['#fc5a03'])
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# --- Data Table ---
st.subheader("Restaurant Data")
st.dataframe(
    filtered_df[['name', 'location', 'rate', 'cost_for_two', 'cuisines', 'rest_type']]
    .reset_index(drop=True)
)

st.divider()
st.subheader("Let's Connect")
st.markdown("""
Built by **Amit Singh** | B.Tech CSE, NSUT Delhi  
📧 [amit.singh.ug23@gmail.com](mailto:amit.singh.ug23@gmail.com)  
🐙 [GitHub](https://github.com/Amitsingh-nsut2027)  
Open to collaborations on Data & ML projects. Feel free to reach out!
""")
st.caption("© 2026 Amit Singh | MIT License | NSUT Delhi")