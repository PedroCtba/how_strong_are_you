import streamlit as st
import plotly.express as px
import pandas as pd
import os
from objects import sex, weight_class, modality, division, federation, country, labels

# Load the OpenPowerlifting data
@st.cache_data(ttl=60*60)
def load_data():
    abs_path = os.path.join(os.getcwd(), "data", "openpowerlifting_clean.parquet")
    df = pd.read_parquet(abs_path)
    return df

@st.cache_data(ttl=300)
def filter_data(df, sex=None, weight_class=None, modality=None, division=None, federation=None, country=None):
    if sex: 
        df = df[df["Sex"] == sex]
    if weight_class: 
        df = df[df["WeightClassKg"] == weight_class]
    if modality: 
        df = df[df["Equipment"] == modality]
    if division: 
        df = df[df["Division"] == division]
    if federation: 
        df = df[df["Federation"] == federation]
    if country: 
        df = df[df["MeetCountry"] == country]
    return df

# Create a function to calculate the user's total
def calculate_total(squat, bench, deadlift):
    return squat + bench + deadlift

# Create a function to plot the user's position
def plot_position(df, lift, user_value, color):
    if df.empty:
        st.error(f"No data available for {lift}")
        return None
    
    fig = px.histogram(df, nbins=100, x=lift, title=f"Distribution of {lift} Values", color_discrete_sequence=[color])
    fig.add_vline(x=user_value, line_dash="dash", line_color="red")
    return fig

# Function to calculate percentile
def calculate_percentile(df, lift, user_value):
    percentile = (df[lift] < user_value).mean() * 100
    return percentile

# Comparison to top group lifters
def compare_to_group(df, user_total, group_percentile=0.9):
    threshold = df["TotalKg"].quantile(group_percentile)
    return "Above" if user_total > threshold else "Below"

# Language selection
lang = st.selectbox("Choose your language / Escolha seu idioma", ["English", "Português"])

# Main app
st.title(labels["title"][lang])

# Get user input based on selected language, allowing "All" or empty inputs
sex = st.selectbox(labels["sex"][lang], ["All"] + sex)
weight_class = st.selectbox(labels["weight_class"][lang], ["All"] + weight_class)
modality = st.selectbox(labels["modality"][lang], ["All"] + modality)
division = st.selectbox(labels["division"][lang], ["All"] + division)
federation = st.selectbox(labels["federation"][lang], ["All"] + federation)
country = st.selectbox(labels["country"][lang], ["All"] + country)

# Convert "All" selections to None for filtering
sex = None if sex == "All" else sex
weight_class = None if weight_class == "All" else weight_class
modality = None if modality == "All" else modality
division = None if division == "All" else division
federation = None if federation == "All" else federation
country = None if country == "All" else country

# Get user lift numbers
squat = st.number_input(labels["squat"][lang], min_value=0, max_value=500, step=1)
bench = st.number_input(labels["bench"][lang], min_value=0, max_value=500, step=1)
deadlift = st.number_input(labels["deadlift"][lang], min_value=0, max_value=500, step=1)

# Load and filter the data
df = load_data()
df = filter_data(df=df, sex=sex, weight_class=weight_class, modality=modality, division=division, federation=federation, country=country)

# Calculate the user's total
user_total = calculate_total(squat, bench, deadlift)

# Only display if all inputs are valid
if squat > 0 and bench > 0 and deadlift > 0:
    st.success(labels["submit"][lang])

    # Plot the user's position for each lift using tabs with different colors
    tab1, tab2, tab3, tab4 = st.tabs(["Squat", "Bench", "Deadlift", "Total"])
    
    with tab1:
        st.plotly_chart(plot_position(df, "Best3SquatKg", squat, "blue"))
    
    with tab2:
        st.plotly_chart(plot_position(df, "Best3BenchKg", bench, "green"))
    
    with tab3:
        st.plotly_chart(plot_position(df, "Best3DeadliftKg", deadlift, "orange"))
    
    with tab4:
        fig = px.histogram(df, x="TotalKg", title=labels["distribution"][lang].format(lift="Total"), color_discrete_sequence=["purple"])
        fig.add_vline(x=user_total, line_dash="dash", line_color="red")
        st.plotly_chart(fig)

    # Calculate the percentile for each lift and total
    total_percentile = calculate_percentile(df, "TotalKg", user_total).round(2)
    squat_percentile = calculate_percentile(df, "Best3SquatKg", squat).round(2)
    bench_percentile = calculate_percentile(df, "Best3BenchKg", bench).round(2)
    deadlift_percentile = calculate_percentile(df, "Best3DeadliftKg", deadlift).round(2)

    # Display the percentile for each lift
    st.subheader(labels["percentile_generic"][lang])
    st.write(labels["percentile_specific"][lang].format(lift=labels["squat"][lang], percentile=squat_percentile))
    st.write(labels["percentile_specific"][lang].format(lift=labels["bench"][lang], percentile=bench_percentile))
    st.write(labels["percentile_specific"][lang].format(lift=labels["deadlift"][lang], percentile=deadlift_percentile))

    # Determine the user's weakest and strongest lift
    weakest_lift = min(squat_percentile, bench_percentile, deadlift_percentile)
    strongest_lift = max(squat_percentile, bench_percentile, deadlift_percentile)

    if squat_percentile == weakest_lift:
        weakest_lift_name = labels["squat"][lang]
    elif bench_percentile == weakest_lift:
        weakest_lift_name = labels["bench"][lang]
    else:
        weakest_lift_name = labels["deadlift"][lang]

    if squat_percentile == strongest_lift:
        strongest_lift_name = labels["squat"][lang]
    elif bench_percentile == strongest_lift:
        strongest_lift_name = labels["bench"][lang]
    else:
        strongest_lift_name = labels["deadlift"][lang]

    st.subheader(labels["weakest_strongest"][lang])
    st.write(f"{labels["weakest"][lang]} {weakest_lift_name}")
    st.write(f"{labels["strongest"][lang]} {strongest_lift_name}")

else:
    st.warning(labels["missing_data"][lang])
