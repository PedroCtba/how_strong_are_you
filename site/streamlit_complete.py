
import streamlit as st
import plotly.express as px
import pandas as pd

# Load the OpenPowerlifting data
@st.cache_data(ttl=60*60)
def load_data(path=r"C:\Users\PedroMiyasaki\OneDrive - DHAUZ\Área de Trabalho\Projetos\PESSOAL\how_strong_are_you\data\openpowerlifting_clean.csv"):
    # Load the cleaned data from your previous script
    df = pd.read_csv(path, usecols=["Sex", "WeightClassKg", "Equipment", "Best3SquatKg", "Best3BenchKg", "Best3DeadliftKg", "TotalKg"])
    return df

@st.cache_data(ttl=300)  # Cache for 5 minutes
def filter_data(df, sex, weight_class, modality):
    return df.loc[(df["Sex"] == sex) & (df["WeightClassKg"] == weight_class) & (df["Equipment"] == modality)]

# Create a function to calculate the user's total
def calculate_total(squat, bench, deadlift):
    return squat + bench + deadlift

# Create a function to plot the user's position
def plot_position(df, lift, user_value):
    if df.empty:
        st.error(f"No data available for {lift}")
        return None
    
    fig = px.histogram(df, nbins=100, x=lift, title=f"Distribution of {lift} Values")
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

# Main app
st.title("How Strong Are You?")

# Get user input
sex = st.selectbox("Sex", ["M", "F"])
weight_class = st.selectbox("Weight Class", [
    "90", "75", "100", "82.5", "67.5", "110", "125", "93", "83", "60",
    "105", "56", "74", "52", "120", "63", "74.8", "66", "67.1", "82.1",
    "99.7", "89.8", "72", "140", "57", "109.7", "124.7", "120+", "84",
    "84+", "59", "59.8", "67.3", "140+", "124.7+", "125+", "90+", "48",
    "55.7", "60.1", "51.7", "51.9", "82.3", "47"
    ])
modality = st.selectbox("Modality", ["Raw", "Wraps", "Multi-ply", "Single-ply", "Unlimited", "Straps"])
squat = st.slider("Squat (kg)", min_value=0, max_value=500, step=1)
bench = st.slider("Bench (kg)", min_value=0, max_value=500, step=1)
deadlift = st.slider("Deadlift (kg)", min_value=0, max_value=500, step=1)

# Load the data
df = load_data()

# Filter the data
df = filter_data(df=df, sex=sex, weight_class=weight_class, modality=modality)

# Calculate the user's total
user_total = calculate_total(squat, bench, deadlift)

# Only display if all inputs are valid
if squat > 0 and bench > 0 and deadlift > 0:
    st.success("Ready to display results!")

    # Plot the user's position for each lift using tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Squat", "Bench", "Deadlift", "Total"])
    
    with tab1:
        st.plotly_chart(plot_position(df, "Best3SquatKg", squat))
    
    with tab2:
        st.plotly_chart(plot_position(df, "Best3BenchKg", bench))
    
    with tab3:
        st.plotly_chart(plot_position(df, "Best3DeadliftKg", deadlift))
    
    with tab4:
        fig = px.histogram(df, x="TotalKg", title="Distribution of Total Values")
        fig.add_vline(x=user_total, line_dash="dash", line_color="red")
        st.plotly_chart(fig)

    # Display the percentile for each lift
    st.subheader("Your Percentile in Each Lift")
    st.write(f"Squat: {calculate_percentile(df, 'Best3SquatKg', squat):.2f}th percentile")
    st.write(f"Bench: {calculate_percentile(df, 'Best3BenchKg', bench):.2f}th percentile")
    st.write(f"Deadlift: {calculate_percentile(df, 'Best3DeadliftKg', deadlift):.2f}th percentile")

    # Compare to top group of lifters
    comparison = compare_to_group(df, user_total)
    st.subheader(f"Comparison to Top Lifters: {comparison}")

    # Option to download user data as CSV
    user_data = {
        "Sex": sex,
        "Weight Class": weight_class,
        "Modality": modality,
        "Squat": squat,
        "Bench": bench,
        "Deadlift": deadlift,
        "Total": user_total
    }
    df_user = pd.DataFrame([user_data])
    st.download_button("Download your data", df_user.to_csv(index=False), "user_data.csv", "text/csv")
else:
    st.warning("Please enter all your lift values to see your position.")
