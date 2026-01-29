import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.model import train_model, save_model, load_model
    from src.evaluation import evaluate_model
    from src.data_preprocessing import load_and_clean_data
except ImportError:
    pass  # Fallback to embedded functions

# Configuration de la page
st.set_page_config(
    page_title="🌍 Tourism Demand Forecast",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<h1 class="main-header">🌍 Tourism Demand Forecasting Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Génération de données étendues pour la démo
@st.cache_data
def generate_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq="D")
    n = len(dates)
    
    # Simulation réaliste des réservations touristiques
    base = 100
    seasonal = 50 * np.sin(2 * np.pi * np.arange(n) / 365 - np.pi/2)  # Pic en été
    weekly = 20 * np.sin(2 * np.pi * np.arange(n) / 7)  # Weekends plus élevés
    trend = np.linspace(0, 30, n)  # Tendance croissante
    noise = np.random.normal(0, 15, n)
    
    bookings = (base + seasonal + weekly + trend + noise).clip(min=20).astype(int)
    
    df = pd.DataFrame({
        "date": dates,
        "bookings": bookings,
        "temperature": (15 + 15 * np.sin(2 * np.pi * np.arange(n) / 365 - np.pi/2) + np.random.normal(0, 3, n)).astype(int),
        "is_holiday": np.random.choice([0, 1], n, p=[0.9, 0.1]),
        "price": (80 + 20 * np.sin(2 * np.pi * np.arange(n) / 365 - np.pi/2) + np.random.normal(0, 5, n)).astype(int)
    })
    
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
    df["quarter"] = df["date"].dt.quarter

    return df

df = generate_demo_data()

# Add tabs for better organization
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🤖 Prédiction ML", "📈 Analyses Avancées", "ℹ️ À Propos"])

with tab1:

    # Sidebar pour les filtres
    st.sidebar.header("🔧 Configuration")
    st.sidebar.markdown("---")

    # Sélection de la période
    date_range = st.sidebar.date_input(
        "📅 Période d'analyse",
        value=(df["date"].min(), df["date"].max()),
        min_value=df["date"].min(),
        max_value=df["date"].max()
    )

    # Filtrage des données
    if len(date_range) == 2:
        mask = (df["date"] >= pd.Timestamp(date_range[0])) & (df["date"] <= pd.Timestamp(date_range[1]))
        df_filtered = df[mask]
    else:
        df_filtered = df

    # Métriques clés
    st.subheader("📊 Métriques Clés")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📈 Total Réservations",
            value=f"{df_filtered['bookings'].sum():,}",
            delta=f"+{int(df_filtered['bookings'].mean())} avg/jour"
        )
    with col2:
        st.metric(
            label="🌡️ Température Moyenne",
            value=f"{df_filtered['temperature'].mean():.1f}°C"
        )
    with col3:
        st.metric(
            label="💰 Prix Moyen",
            value=f"{df_filtered['price'].mean():.0f}€"
        )
    with col4:
        st.metric(
            label="🎉 Jours Fériés",
            value=f"{df_filtered['is_holiday'].sum()} jours"
        )

    st.markdown("---")

    # Graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📈 Évolution des Réservations")
        fig_line = px.line(
            df_filtered,
            x="date",
            y="bookings",
            title="Demande Touristique au Fil du Temps",
            labels={"date": "Date", "bookings": "Réservations"}
        )
        fig_line.update_traces(line_color="#667eea")
        fig_line.update_layout(hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("🌡️ Température vs Réservations")
        fig_scatter = px.scatter(
            df_filtered,
            x="temperature",
            y="bookings",
            color="is_holiday",
            title="Corrélation Température-Demande",
            labels={"temperature": "Température (°C)", "bookings": "Réservations", "is_holiday": "Jour Férié"},
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

    # Additional visualizations
    col_viz1, col_viz2 = st.columns(2)

    with col_viz1:
        st.subheader("📅 Réservations par Mois")
        monthly_bookings = df_filtered.groupby("month")["bookings"].mean().reset_index()
        fig_monthly = px.bar(
            monthly_bookings,
            x="month",
            y="bookings",
            title="Moyenne des Réservations par Mois",
            labels={"month": "Mois", "bookings": "Réservations Moyennes"},
            color="bookings",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    with col_viz2:
        st.subheader("📆 Réservations par Jour de la Semaine")
        dow_bookings = df_filtered.groupby("day_of_week")["bookings"].mean().reset_index()
        dow_bookings["day_name"] = dow_bookings["day_of_week"].map({
            0: "Lun", 1: "Mar", 2: "Mer", 3: "Jeu", 4: "Ven", 5: "Sam", 6: "Dim"
        })
        fig_dow = px.bar(
            dow_bookings,
            x="day_name",
            y="bookings",
            title="Moyenne des Réservations par Jour",
            labels={"day_name": "Jour", "bookings": "Réservations Moyennes"},
            color="bookings",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig_dow, use_container_width=True)

    st.markdown("---")

with tab2:
    # Section Prédiction
    st.subheader("🤖 Prédiction avec Machine Learning")

    col_pred1, col_pred2 = st.columns([1, 2])

    with col_pred1:
        st.markdown("### Paramètres de Prédiction")

        pred_temp = st.slider("🌡️ Température (°C)", min_value=-5, max_value=40, value=20)
        pred_holiday = st.selectbox("🎉 Jour Férié?", options=[0, 1], format_func=lambda x: "Oui" if x == 1 else "Non")
        pred_price = st.slider("💰 Prix (€)", min_value=50, max_value=150, value=90)
        pred_month = st.selectbox("📅 Mois", options=list(range(1, 13)), index=6)
        pred_dow = st.selectbox("📆 Jour de la semaine", options=list(range(7)),
                               format_func=lambda x: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][x])

        # Entraînement du modèle
        @st.cache_resource
        def train_model_simple(df):
            X = df[["temperature", "is_holiday", "price", "month", "day_of_week"]]
            y = df["bookings"]
            model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=15)
            model.fit(X, y)
            return model

        model = train_model_simple(df)

        # Prédiction
        input_data = pd.DataFrame({
            "temperature": [pred_temp],
            "is_holiday": [pred_holiday],
            "price": [pred_price],
            "month": [pred_month],
            "day_of_week": [pred_dow]
        })

        prediction = model.predict(input_data)[0]

        st.markdown("### 📊 Résultat de la Prédiction")

        # Gauge chart pour la prédiction
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=prediction,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Réservations Prédites", 'font': {'size': 20}},
            delta={'reference': df["bookings"].mean(), 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [None, 250], 'tickwidth': 1},
                'bar': {'color': "#667eea"},
                'bgcolor': "white",
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 80], 'color': '#ffcdd2'},
                    {'range': [80, 150], 'color': '#fff9c4'},
                    {'range': [150, 250], 'color': '#c8e6c9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': df["bookings"].mean()
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.markdown("---")

    # Feature Importance
    st.subheader("🎯 Importance des Variables")

    feature_importance = pd.DataFrame({
        "Feature": ["Température", "Jour Férié", "Prix", "Mois", "Jour de semaine"],
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=True)

    fig_importance = px.bar(
        feature_importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Facteurs Influençant la Demande Touristique",
        color="Importance",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_importance, use_container_width=True)

with tab3:
    st.subheader("📈 Analyses Statistiques Avancées")

    col_stat1, col_stat2 = st.columns(2)

    with col_stat1:
        st.markdown("### 📊 Matrice de Corrélation")
        corr_data = df[["bookings", "temperature", "price", "is_holiday", "month", "day_of_week"]].corr()
        fig_corr = px.imshow(
            corr_data,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Corrélations entre Variables"
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    with col_stat2:
        st.markdown("### 📉 Distribution des Réservations")
        fig_hist = px.histogram(
            df,
            x="bookings",
            nbins=30,
            title="Distribution des Réservations",
            labels={"bookings": "Réservations", "count": "Fréquence"},
            color_discrete_sequence=["#667eea"]
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("---")

    # Box plots
    col_box1, col_box2 = st.columns(2)

    with col_box1:
        st.markdown("### 📦 Réservations par Jour Férié")
        fig_box1 = px.box(
            df,
            x="is_holiday",
            y="bookings",
            title="Comparaison Jour Normal vs Férié",
            labels={"is_holiday": "Jour Férié", "bookings": "Réservations"},
            color="is_holiday"
        )
        st.plotly_chart(fig_box1, use_container_width=True)

    with col_box2:
        st.markdown("### 📦 Réservations par Trimestre")
        fig_box2 = px.box(
            df,
            x="quarter",
            y="bookings",
            title="Réservations par Trimestre",
            labels={"quarter": "Trimestre", "bookings": "Réservations"},
            color="quarter"
        )
        st.plotly_chart(fig_box2, use_container_width=True)

with tab4:
    st.subheader("ℹ️ À Propos du Projet")

    st.markdown("""
    ### 🌍 Tourism Demand Forecasting

    Cette application utilise le Machine Learning pour prédire la demande touristique basée sur plusieurs facteurs.

    #### 📊 Fonctionnalités

    - **Dashboard Interactif**: Visualisez les tendances historiques et les métriques clés
    - **Prédictions ML**: Utilisez Random Forest pour prédire les réservations futures
    - **Analyses Avancées**: Explorez les corrélations et distributions statistiques
    - **Feature Engineering**: Extraction automatique de features temporelles

    #### 🛠️ Technologies Utilisées

    - Python 3.12
    - Streamlit (Dashboard)
    - Scikit-learn (Machine Learning)
    - Plotly (Visualisations)
    - Pandas & NumPy (Data Processing)

    #### 📈 Métriques d'Évaluation

    Le modèle est évalué avec:
    - **MAE** (Mean Absolute Error)
    - **RMSE** (Root Mean Squared Error)
    - **R²** (Coefficient de Détermination)
    - **MAPE** (Mean Absolute Percentage Error)

    #### 🎯 Features Utilisées

    1. Température
    2. Jour Férié
    3. Prix
    4. Mois
    5. Jour de la semaine
    6. Trimestre
    7. Weekend
    8. Features cycliques (sin/cos)

    #### 👨‍💻 Développé par zaka41a

    Version 2.0 - Enhanced Edition
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🛠️ Développé avec Python, Scikit-learn & Streamlit</p>
    <p>📊 Projet: Tourism Demand Forecasting | Data Science & KI</p>
</div>
""", unsafe_allow_html=True)
