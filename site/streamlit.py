import streamlit as st
import plotly.express as px
import pandas as pd
import os
from objects import sex, weight_class, modality, division, federation, country, labels

# Load the OpenPowerlifting data
@st.cache_data(ttl=60*60)
def load_data():
    abs_path = os.path.join(os.getcwd(), "data", "openpowerlifting_clean.parquet")
    columns = ["Sex", "WeightClassKg", "Equipment", "Division", "Federation", "MeetCountry", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "TotalKg"]
    df = pd.read_parquet(abs_path, columns=columns)
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

# Create a function to plot the user's position with language-based labels and improved aesthetics
def plot_position(df, lift, user_value, color, lang, y_label=None, x_label=None):
    if df.empty:
        st.error(f"No data available for {lift}")
        return None
    
    # Set default labels in both languages
    y_label = y_label or (labels["y_axis_label"][lang] if "y_axis_label" in labels else "Frequency")
    x_label = x_label or lift

    # Text for the "You are here" annotation in both languages
    annotation_text = "Você está aqui" if lang == "Português" else "You are here"
    
    # Create a customized histogram plot
    fig = px.histogram(df, nbins=100, x=lift, title=labels["distribution"][lang].format(lift=lift), color_discrete_sequence=[color])
    
    # Add vertical line to represent user value
    fig.add_vline(x=user_value, line_dash="dash", line_color="red", annotation_text=annotation_text, 
                  annotation_position="top right")
    
    # Customize layout for better aesthetics
    fig.update_layout(
        title_font_size=20,
        xaxis_title=x_label,  # Use the translated x-axis label
        yaxis_title=y_label,  # Use the translated y-axis label
        font=dict(family="Arial", size=14, color="black"),
        plot_bgcolor="rgba(0, 0, 0, 0)",  # Transparent background
        paper_bgcolor="rgba(0, 0, 0, 0)",  # Transparent paper background
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(showgrid=False),  # Hide vertical grid lines
        yaxis=dict(showgrid=True, gridcolor="lightgray"),  # Light gray horizontal grid lines
        title_x=0.5,  # Center title
    )
    
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

    # Plot the user's position for each lift using tabs with different colors and language-based labels
    tab1, tab2, tab3, tab4 = st.tabs([labels["squat"][lang], labels["bench"][lang], labels["deadlift"][lang], "Total")
    
    with tab1:
        st.plotly_chart(plot_position(df, "Best3SquatKg", squat, "blue", lang, x_label=labels["squat"][lang]))
    
    with tab2:
        st.plotly_chart(plot_position(df, "Best3BenchKg", bench, "green", lang, x_label=labels["bench"][lang]))
    
    with tab3:
        st.plotly_chart(plot_position(df, "Best3DeadliftKg", deadlift, "orange", lang, x_label=labels["deadlift"][lang]))
    
    with tab4:
        fig = plot_position(df, "TotalKg", user_total, "purple", lang, x_label="Total")
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
