# Instanciar listas para os seletores (Sex)
sex = ["M", "F"]

# Instanciar listas para os seletores (weight class)
weight_class = [
    "90", "75", "100", "82.5", 
    "67.5", "110", "125", "93", 
    "83", "60", "105", "56", "74", 
    "52", "120", "63", "74.8", "66"
]

# Instanciar listas para os seletores (modality)
modality = ["Raw", "Wraps", "Multi-ply", "Single-ply", "Unlimited", "Straps"]

# Instanciar listas para os seletores (division)
division = ["Open", "Juniors", "MR-O", "Amateur Open", "Pro Open", "Sub-Juniors",
       "Masters 1", "FR-O", "Juniors 20-23", "O", "M-O", "Masters 2", "MR-Jr",
       "Masters 40-44", "Masters 45-49", "Masters 3", "Amateur Juniors 20-23",
       "Submasters 35-39", "Novice", "Masters 50-54", "F-O", "Teen",
       "M-C-Open", "Masters 40-49", "FR-Jr", "Teen 16-17", "M-OR",
       "Masters 55-59", "Juniors 19-23", "J", "Pro Juniors 20-23", "MR-T3",
       "Teen 18-19", "Juniors 18-19", "Junior", "Seniors", "MR-C",
       "Teen 14-18", "High School"]

# Instanciar listas para os seletores (federation)
federation = ["THSPA", "USAPL", "FPR", "USPA", "THSWPA", "USPF", "WPC-RUS", "APF",
       "CPU", "WRPF", "IPF", "WPC", "NSF", "WABDL", "RPS", "NAP", "BVDK",
       "NASA", "RPU", "EPF", "SVNL", "EPA", "FFForce", "UkrainePF", "SPF",
       "PA", "CSST", "SSF", "ADFPA", "JPA", "FIPL", "AAU", "RAW", "IPA", "IPL",
       "WDFPF", "GPC", "NZPF", "BAWLA"]

# Instanciar listas para os seletores (pais)
country = ["USA", "Russia", "Ukraine", "Canada", "Australia", "Germany", "England",
       "Norway", "Finland", "Czechia", "France", "Sweden", "Italy", "UK",
       "Poland", "Japan", "New Zealand", "Denmark", "Ireland", "Hungary",
       "India", "Kazakhstan", "Netherlands", "Argentina", "Belgium",
       "Slovakia", "Spain", "South Africa", "Belarus", "Lithuania", "Scotland",
       "Iceland", "Austria", "Brazil", "Greece", "Estonia", "China", "Mexico",
       "Croatia", "Switzerland", "UAE", "Luxembourg", "Romania",
       "West Germany", "Wales", "N.Ireland", "Philippines", "Latvia", "Israel",
       "Costa Rica", "Serbia", "Turkey", "Malaysia", "Bulgaria", "Portugal",
       "USSR", "Slovenia"]

# Define labels and text in both languages
labels = {
    "title": {"English": "How Strong Are You?","Português": "Quão Forte Você é?"},
    "sex": {"English": "Sex", "Português": "Sexo"},
    "weight_class": {"English": "Weight Class", "Português": "Classe de Peso"},
    "modality": {"English": "Modality", "Português": "Modalidade"},
    "division": {"English": "Division", "Português": "Divisão"},
    "federation": {"English": "Federation", "Português": "Federação"},
    "country": {"English": "Country", "Português": "País"},
    "squat": {"English": "Squat", "Português": "Agachamento"},
    "bench": {"English": "Bench", "Português": "Supino"},
    "deadlift": {"English": "Deadlift", "Português": "Levantamento Terra"},
    "submit": {"English": "Ready to display results!", "Português": "Pronto para exibir os resultados!"},
    "missing_data": {"English": "Please, fill in the filters to see better comparisons and results.",
                     "Português": "Por favor, preencha os filtros para visualizar melhores comparacões e resultados."},
    "distribution": {"English": "Distribution of {lift} Values", "Português": "Distribuição dos Valores de {lift}"},
    "percentile_generic": {"English": "Your relative performance on each lift", "Português": "Sua performance relativa em cada levantamento"},
    "percentile_specific": {"English": "Your {lift} is better than {percentile}% of the filtered atheltes", "Português": "Seu {lift} é melhor que {percentile}% dos atletas filtrados"},
    "comparison": {"English": "Comparison to Top Lifters", "Português": "Comparação com os Melhores Levantadores"},
    "weakest_strongest": {
            "English": "Weakest and Strongest Lifts:",
            "Português": "Melhor e pior levantamento:"},
    "weakest": {
            "English": "Weakest lift:",
            "Português": "Pior levantamento:"},
    "strongest": {
            "English": "Strongest Lift:",
            "Português": "Melhor Levantamento:"},
    "y_axis_label": {
        "English": "Frequency",
        "Português": "Frequência"},
    "filter_all": {
        "English": "All",
        "Português": "Todos"},
    }
