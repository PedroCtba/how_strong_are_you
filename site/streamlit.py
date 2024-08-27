import streamlit as st
import plotly.express as px
import pandas as pd

# Load the OpenPowerlifting data
@st.cache_data(ttl=60*60)
def load_data(path=r"C:\\Users\\PedroMiyasaki\\OneDrive - DHAUZ\\Área de Trabalho\\Projetos\\PESSOAL\\how_strong_are_you\\data\\openpowerlifting_clean.pkl"):
    df = pd.read_pickle(path)
    return df

@st.cache_data(ttl=300)
def filter_data(df, sex, weight_class, modality):
    return df.loc[(df["Sex"] == sex) & (df["WeightClassKg"] == weight_class) & (df["Equipment"] == modality)]

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

# Define labels and text in both languages
labels = {
    "title": {"English": "How Strong Are You?","Português": "Quão Forte Você é?"},
    "sex": {"English": "Sex", "Português": "Sexo"},
    "weight_class": {"English": "Weight Class", "Português": "Classe de Peso"},
    "modality": {"English": "Modality", "Português": "Modalidade"},
    "squat": {"English": "Squat", "Português": "Agachamento"},
    "bench": {"English": "Bench", "Português": "Supino"},
    "deadlift": {"English": "Deadlift", "Português": "Levantamento Terra"},
    "submit": {"English": "Ready to display results!", "Português": "Pronto para exibir os resultados!"},
    "missing_data": {"English": "Please enter all your lift values to see your position.",
                     "Português": "Por favor, insira todos os valores para visualizar sua posição."},
    "distribution": {"English": "Distribution of {lift} Values", "Português": "Distribuição dos Valores de {lift}"},
    "percentile": {"English": "Your Percentile in Each Lift", "Português": "Seu Percentil em Cada Levantamento"},
    "comparison": {"English": "Comparison to Top Lifters", "Português": "Comparação com os Melhores Levantadores"},
    "weakest_strongest": {
            "English": "Weakest and Strongest Lifts Relative to percentile",
            "Português": "Melhor e pior levantamento relativo ao percentil"}
    }

# Main app
st.title(labels["title"][lang])

# Get user input based on selected language
sex = st.selectbox(labels["sex"][lang], ["M", "F"])
weight_class = st.selectbox(labels["weight_class"][lang], [
    "90", "75", "100", "82.5", "67.5", "110", "125", "93", "83", "60",
    "105", "56", "74", "52", "120", "63", "74.8", "66"
])
modality = st.selectbox(labels["modality"][lang], ["Raw", "Wraps", "Multi-ply", "Single-ply", "Unlimited", "Straps"])
squat = st.number_input(labels["squat"][lang], min_value=0, max_value=500, step=1)
bench = st.number_input(labels["bench"][lang], min_value=0, max_value=500, step=1)
deadlift = st.number_input(labels["deadlift"][lang], min_value=0, max_value=500, step=1)

# Load and filter the data
df = load_data()
df = filter_data(df=df, sex=sex, weight_class=weight_class, modality=modality)

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

    # Calculate the percentile for each lift
    squat_percentile = calculate_percentile(df, "Best3SquatKg", squat).round(2)
    bench_percentile = calculate_percentile(df, "Best3BenchKg", bench).round(2)
    deadlift_percentile = calculate_percentile(df, "Best3DeadliftKg", deadlift).round(2)

    # Display the percentile for each lift
    st.subheader(labels["percentile"][lang])
    st.write(f"Squat: {squat_percentile}th percentile")
    st.write(f"Bench: {bench_percentile}th percentile")
    st.write(f"Deadlift: {deadlift_percentile}th percentile")

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
    st.write(f"Weakest Lift: {weakest_lift_name}")
    st.write(f"Strongest Lift: {strongest_lift_name})")

else:
    st.warning(labels["missing_data"][lang])