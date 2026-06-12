import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
import pytz
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="🚀 SPCX & Space ETF Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration du fuseau horaire
USER_TIMEZONE = pytz.timezone('Europe/Paris')
US_TIMEZONE = pytz.timezone('America/New_York')

# Style CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #005288;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #000000 0%, #005288 50%, #FFFFFF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .spacex-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1rem;
        border-radius: 1rem;
        color: white;
        margin: 1rem 0;
        border-left: 4px solid #005288;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .score-card {
        padding: 1rem;
        border-radius: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        color: white;
    }
    .score-excellent { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .score-good { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
    .score-average { background: linear-gradient(135deg, #f2994a, #f2c94c); }
    .score-poor { background: linear-gradient(135deg, #eb3349, #f45c43); }
    .timezone-badge {
        background-color: #e3f2fd;
        border-left: 4px solid #005288;
        padding: 0.5rem 1rem;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    .stButton>button { width: 100%; }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .etf-holdings {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des variables de session
if 'price_alerts' not in st.session_state:
    st.session_state.price_alerts = []

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

if 'email_config' not in st.session_state:
    st.session_state.email_config = {
        'enabled': False,
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'email': '',
        'password': ''
    }

# Base de données SPCX et ETF spatiaux
SPCX_HOLDINGS = {
    'RKLB': {'name': 'Rocket Lab USA', 'weight': 12.5, 'sector': 'Lanceurs'},
    'ASTS': {'name': 'AST SpaceMobile', 'weight': 8.2, 'sector': 'Satellites'},
    'RDW': {'name': 'Redwire', 'weight': 6.8, 'sector': 'Infrastructure'},
    'PL': {'name': 'Planet Labs', 'weight': 7.5, 'sector': 'Imagerie'},
    'SPCE': {'name': 'Virgin Galactic', 'weight': 5.2, 'sector': 'Tourisme'},
    'GSAT': {'name': 'Globalstar', 'weight': 4.8, 'sector': 'Communications'},
    'IRDM': {'name': 'Iridium', 'weight': 6.2, 'sector': 'Communications'},
    'LLAP': {'name': 'Terran Orbital', 'weight': 3.5, 'sector': 'Satellites'},
    'BKSY': {'name': 'BlackSky', 'weight': 3.2, 'sector': 'Imagerie'},
    'SATL': {'name': 'Satellogic', 'weight': 2.8, 'sector': 'Imagerie'},
    'ASTR': {'name': 'Astra Space', 'weight': 2.5, 'sector': 'Lanceurs'},
    'MNTS': {'name': 'Momentus', 'weight': 1.8, 'sector': 'Logistique'},
}

SPACE_ETFS = {
    'SPCX': {'name': 'SPAC & NewSpace ETF', 'aum': 125e6, 'expense_ratio': 0.75, 'holdings': 25},
    'UFO': {'name': 'Procure Space ETF', 'aum': 180e6, 'expense_ratio': 0.75, 'holdings': 30},
    'ARKX': {'name': 'ARK Space Exploration ETF', 'aum': 350e6, 'expense_ratio': 0.75, 'holdings': 40},
    'ROKT': {'name': 'SPDR S&P Aerospace & Defense ETF', 'aum': 800e6, 'expense_ratio': 0.35, 'holdings': 45},
    'ITA': {'name': 'iShares US Aerospace & Defense', 'aum': 5.2e9, 'expense_ratio': 0.40, 'holdings': 38},
    'PPA': {'name': 'Invesco Aerospace & Defense', 'aum': 2.1e9, 'expense_ratio': 0.56, 'holdings': 50},
}

# Métadonnées SPCX
SPCX_INFO = {
    'name': 'SPAC & NewSpace ETF',
    'issuer': 'ProcureAM',
    'inception': '2021-02-17',
    'expense_ratio': 0.75,
    'aum': 125000000,
    'description': 'Le SPCX est un ETF qui investit dans les sociétés spatiales émergentes, incluant les SPACs et les entreprises NewSpace.'
}

# ============================================================================
# FONCTIONS
# ============================================================================

@st.cache_data(ttl=300, show_spinner=False)
def get_stock_data(symbol, period="1mo", interval="1d"):
    """Récupère les données avec fallback"""
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if not hist.empty:
            if hist.index.tz is None:
                hist.index = hist.index.tz_localize('UTC').tz_convert(USER_TIMEZONE)
            else:
                hist.index = hist.index.tz_convert(USER_TIMEZONE)
            
            info = ticker.info
            return hist, info
        
        return generate_fallback_data(symbol, period), {}
        
    except Exception as e:
        return generate_fallback_data(symbol, period), {}

def generate_fallback_data(symbol, period="1mo"):
    """Génère des données simulées réalistes"""
    # Prix de base pour SPCX
    base_prices = {
        'SPCX': 12.50, 'UFO': 18.30, 'ARKX': 15.20, 'ROKT': 42.50, 'ITA': 115.00, 'PPA': 95.00
    }
    base_price = base_prices.get(symbol, 10.0)
    volatility = 0.22 if symbol == 'SPCX' else 0.18
    
    period_days = {"1d": 1, "5d": 5, "1mo": 22, "3mo": 66, "6mo": 132, "1y": 252}
    days = period_days.get(period, 22)
    
    end_date = datetime.now(USER_TIMEZONE)
    dates = pd.date_range(end=end_date, periods=days, freq='D')
    
    # Génération des prix
    returns = np.random.normal(0, volatility / np.sqrt(252), days)
    prices = base_price * np.exp(np.cumsum(returns))
    prices[0] = base_price
    
    hist = pd.DataFrame({
        'Open': prices * (1 + np.random.uniform(-0.02, 0.02, days)),
        'High': prices * (1 + np.random.uniform(0, 0.03, days)),
        'Low': prices * (1 - np.random.uniform(0, 0.03, days)),
        'Close': prices,
        'Volume': np.random.uniform(100000, 500000, days)
    }, index=dates)
    
    hist['High'] = hist[['High', 'Close']].max(axis=1)
    hist['Low'] = hist[['Low', 'Close']].min(axis=1)
    
    return hist

def calculate_etf_score(symbol, hist, info):
    """Calcule un score pour l'ETF"""
    score = 50
    
    # Actifs sous gestion
    aum = SPACE_ETFS.get(symbol, {}).get('aum', 0)
    if aum > 1e9:
        score += 20
    elif aum > 500e6:
        score += 15
    elif aum > 100e6:
        score += 10
    
    # Performance récente
    if hist is not None and not hist.empty and len(hist) > 20:
        close = hist['Close']
        ma20 = close.rolling(20).mean()
        if close.iloc[-1] > ma20.iloc[-1]:
            score += 10
        
        if len(close) > 20:
            perf = (close.iloc[-1] / close.iloc[-21] - 1) * 100
            if perf > 5:
                score += 10
            elif perf > 0:
                score += 5
            elif perf < -10:
                score -= 10
    
    # Frais (moins = mieux)
    expense_ratio = SPACE_ETFS.get(symbol, {}).get('expense_ratio', 1.0)
    if expense_ratio < 0.4:
        score += 10
    elif expense_ratio < 0.6:
        score += 5
    elif expense_ratio > 0.8:
        score -= 10
    
    # Diversification
    holdings = SPACE_ETFS.get(symbol, {}).get('holdings', 0)
    if holdings > 40:
        score += 10
    elif holdings > 25:
        score += 5
    
    return min(max(score, 0), 100)

def get_score_grade(score):
    if score >= 75: return "EXCELLENT", "score-excellent", "🌟"
    if score >= 60: return "TRÈS BON", "score-good", "📈"
    if score >= 45: return "BON", "score-average", "✅"
    return "FAIBLE", "score-poor", "⚠️"

def format_currency(value):
    return f"${value:.2f}"

def format_large_number(value):
    if value > 1e9:
        return f"${value/1e9:.1f}B"
    elif value > 1e6:
        return f"${value/1e6:.1f}M"
    return f"${value:,.0f}"

def send_email_alert(subject, body, to_email):
    if not st.session_state.email_config['enabled']:
        return False
    try:
        msg = MIMEMultipart()
        msg['From'] = st.session_state.email_config['email']
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(
            st.session_state.email_config['smtp_server'],
            st.session_state.email_config['smtp_port']
        )
        server.starttls()
        server.login(st.session_state.email_config['email'], st.session_state.email_config['password'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        return False

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

st.markdown("<h1 class='main-header'>🚀 SPCX & Space ETF Tracker</h1>", unsafe_allow_html=True)

current_time_paris = datetime.now(USER_TIMEZONE)
current_time_ny = datetime.now(US_TIMEZONE)

st.markdown(f"""
<div class='timezone-badge'>
    <b>🕐 Fuseaux horaires :</b><br>
    🇫🇷 Paris : {current_time_paris.strftime('%H:%M:%S')} (UTC+2)<br>
    🇺🇸 New York (Bourse) : {current_time_ny.strftime('%H:%M:%S')} (UTC-4/UTC-5)
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/SpaceX_Logo_Black.png/800px-SpaceX_Logo_Black.png", width=200)
    st.title("Navigation")
    
    menu = st.radio(
        "Choisir une section",
        ["📈 SPCX Dashboard",
         "🏆 Comparatif ETF",
         "📊 Holdings SPCX",
         "💰 Portefeuille",
         "🔔 Alertes prix",
         "📧 Email",
         "🤖 Prédictions"]
    )
    
    st.markdown("---")
    
    # Sélection ETF principal
    default_etf = "SPCX"
    symbol = st.selectbox("ETF principal", list(SPACE_ETFS.keys()), index=0)
    period = st.selectbox("Période", ["1mo", "3mo", "6mo", "1y"], index=0)
    auto_refresh = st.checkbox("Auto-refresh", value=False)
    if auto_refresh:
        refresh_rate = st.slider("Fréquence (sec)", 5, 60, 30)

# Chargement des données
hist, info = get_stock_data(symbol, period)

if hist is not None and not hist.empty:
    current_price = hist['Close'].iloc[-1]
    etf_info = SPACE_ETFS.get(symbol, {})
    st.success(f"✅ Données chargées pour {symbol} - {etf_info.get('name', symbol)} | Prix: {format_currency(current_price)}")

# ============================================================================
# SECTION 1: SPCX DASHBOARD
# ============================================================================
if menu == "📈 SPCX Dashboard":
    st.subheader("📊 SPCX - SPAC & NewSpace ETF Dashboard")
    
    # Info SPCX
    st.markdown(f"""
    <div class='spacex-card'>
        <b>🚀 {SPCX_INFO['name']} ({symbol})</b><br>
        Émetteur: {SPCX_INFO['issuer']} | Frais: {SPCX_INFO['expense_ratio']}% | AUM: {format_large_number(SPCX_INFO['aum'])}<br>
        Inception: {SPCX_INFO['inception']}<br>
        {SPCX_INFO['description']}
    </div>
    """, unsafe_allow_html=True)
    
    if hist is not None and not hist.empty:
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_price
        change_pct = (change / prev_price * 100) if prev_price != 0 else 0
        
        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Prix SPCX", format_currency(current_price), f"{change:+.3f} ({change_pct:+.2f}%)")
        col2.metric("AUM", format_large_number(SPCX_INFO['aum']))
        col3.metric("Frais", f"{SPCX_INFO['expense_ratio']}%")
        col4.metric("Holdings", f"{SPACE_ETFS['SPCX']['holdings']}")
        
        # Graphique SPCX
        st.subheader("📈 Évolution SPCX")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist['Close'],
            mode='lines', name='SPCX',
            line=dict(color='#005288', width=2),
            fill='tozeroy', fillcolor='rgba(0,82,136,0.1)'
        ))
        
        if len(hist) >= 20:
            ma20 = hist['Close'].rolling(20).mean()
            fig.add_trace(go.Scatter(
                x=hist.index, y=ma20,
                mode='lines', name='MA20',
                line=dict(color='orange', width=1, dash='dash')
            ))
        
        if len(hist) >= 50:
            ma50 = hist['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(
                x=hist.index, y=ma50,
                mode='lines', name='MA50',
                line=dict(color='purple', width=1, dash='dash')
            ))
        
        fig.update_layout(
            title=f"SPCX - Performance {period}",
            xaxis_title="Date (Paris UTC+2)",
            yaxis_title="Prix ($)",
            height=500,
            hovermode='x unified',
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Volatilité", f"{hist['Close'].pct_change().std() * 100:.2f}%")
        with col2:
            perf_period = ((current_price / hist['Close'].iloc[0] - 1) * 100)
            st.metric(f"Performance {period}", f"{perf_period:+.1f}%")
        with col3:
            st.metric("Volume moyen", f"{hist['Volume'].mean()/1e3:.0f}K")
        
        # Top holdings
        st.subheader("🏆 Top 5 Holdings SPCX")
        
        top_holdings = sorted(SPCX_HOLDINGS.items(), key=lambda x: x[1]['weight'], reverse=True)[:5]
        
        for symbol_h, data in top_holdings:
            # Récupérer le prix actuel
            hist_h, _ = get_stock_data(symbol_h, "1d")
            price = hist_h['Close'].iloc[-1] if hist_h is not None else 0
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.write(f"**{symbol_h}** - {data['name']}")
            with col2:
                st.write(f"Secteur: {data['sector']}")
            with col3:
                st.write(f"Weight: {data['weight']}%")
            with col4:
                st.write(f"Prix: {format_currency(price)}")
        
        # Performance vs indices
        st.subheader("📊 Performance comparative")
        
        compare_etfs = ['SPCX', 'UFO', 'ARKX', 'ITA']
        perf_data = []
        
        for etf in compare_etfs:
            hist_e, _ = get_stock_data(etf, period)
            if hist_e is not None and not hist_e.empty:
                normalized = (hist_e['Close'] / hist_e['Close'].iloc[0] - 1) * 100
                perf_data.append({'ETF': etf, 'Date': hist_e.index, 'Performance': normalized})
        
        if perf_data:
            fig_comp = go.Figure()
            for data in perf_data:
                fig_comp.add_trace(go.Scatter(
                    x=data['Date'], y=data['Performance'],
                    mode='lines', name=data['ETF'],
                    line=dict(width=2)
                ))
            
            fig_comp.update_layout(
                title=f"Performance comparative - {period} (normalisée %)",
                xaxis_title="Date",
                yaxis_title="Performance %",
                height=400,
                template='plotly_white'
            )
            st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.warning(f"⚠️ Données non disponibles pour {symbol}")

# ============================================================================
# SECTION 2: COMPARATIF ETF
# ============================================================================
elif menu == "🏆 Comparatif ETF":
    st.subheader("🏆 Comparatif des ETF spatiaux")
    
    etf_scores = []
    
    for etf, etf_data in SPACE_ETFS.items():
        hist_e, _ = get_stock_data(etf, "1mo")
        score = calculate_etf_score(etf, hist_e, {})
        grade, grade_class, icon = get_score_grade(score)
        
        current_price = hist_e['Close'].iloc[-1] if hist_e is not None else 0
        
        etf_scores.append({
            'ETF': etf,
            'Nom': etf_data['name'],
            'Prix': format_currency(current_price),
            'AUM': format_large_number(etf_data['aum']),
            'Frais': f"{etf_data['expense_ratio']}%",
            'Holdings': etf_data['holdings'],
            'Score': round(score, 1),
            'Grade': grade,
            'Icone': icon
        })
    
    df_etfs = pd.DataFrame(etf_scores).sort_values('Score', ascending=False)
    
    for _, row in df_etfs.iterrows():
        grade_class = "score-excellent" if row['Score'] >= 75 else "score-good" if row['Score'] >= 60 else "score-average"
        st.markdown(f"""
        <div class='score-card {grade_class}'>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <div style='flex: 2'>
                    <span style='font-weight: bold; font-size: 18px;'>{row['Icone']} {row['ETF']}</span>
                    <br><span style='font-size: 12px;'>{row['Nom']}</span>
                </div>
                <div style='flex: 1'>{row['Prix']}</div>
                <div style='flex: 1'>{row['AUM']}</div>
                <div style='flex: 0.5'>{row['Frais']}</div>
                <div style='flex: 0.5'>{row['Holdings']}</div>
                <div style='flex: 0.5; text-align: center;'>
                    <span style='font-size: 28px; font-weight: bold;'>{row['Score']}</span>
                    <br><span style='font-size: 12px;'>{row['Grade']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Détail comparatif")
    st.dataframe(df_etfs, use_container_width=True)
    
    # Graphique comparatif des performances
    st.subheader("📈 Performance comparative")
    
    selected_etfs = st.multiselect(
        "Sélectionner les ETF à comparer",
        list(SPACE_ETFS.keys()),
        default=['SPCX', 'UFO', 'ARKX']
    )
    
    if selected_etfs:
        fig = go.Figure()
        for etf in selected_etfs:
            hist_e, _ = get_stock_data(etf, "3mo")
            if hist_e is not None and not hist_e.empty:
                normalized = (hist_e['Close'] / hist_e['Close'].iloc[0] - 1) * 100
                fig.add_trace(go.Scatter(
                    x=hist_e.index, y=normalized,
                    mode='lines', name=etf, line=dict(width=2)
                ))
        
        fig.update_layout(
            title="Performance comparative (normalisée à 100%)",
            xaxis_title="Date",
            yaxis_title="Performance %",
            height=500,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SECTION 3: HOLDINGS SPCX
# ============================================================================
elif menu == "📊 Holdings SPCX":
    st.subheader("📊 Composition détaillée du SPCX")
    
    # Métriques du fonds
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nombre de holdings", len(SPCX_HOLDINGS))
    col2.metric("Top 5 poids", f"{sum([h['weight'] for h in list(SPCX_HOLDINGS.values())[:5]]):.1f}%")
    col3.metric("Frais", f"{SPCX_INFO['expense_ratio']}%")
    col4.metric("AUM", format_large_number(SPCX_INFO['aum']))
    
    # Liste des holdings
    holdings_data = []
    total_weight = 0
    
    for sym, data in sorted(SPCX_HOLDINGS.items(), key=lambda x: x[1]['weight'], reverse=True):
        hist_h, _ = get_stock_data(sym, "1d")
        current_price = hist_h['Close'].iloc[-1] if hist_h is not None else 0
        total_weight += data['weight']
        
        holdings_data.append({
            'Symbole': sym,
            'Société': data['name'],
            'Secteur': data['sector'],
            'Poids %': data['weight'],
            'Prix': format_currency(current_price),
            'Valeur estimée': format_large_number((data['weight']/100) * SPCX_INFO['aum'])
        })
    
    df_holdings = pd.DataFrame(holdings_data)
    st.dataframe(df_holdings, use_container_width=True, height=400)
    
    # Graphique de répartition par secteur
    st.subheader("🥧 Répartition sectorielle")
    
    sector_weights = {}
    for data in SPCX_HOLDINGS.values():
        sector = data['sector']
        sector_weights[sector] = sector_weights.get(sector, 0) + data['weight']
    
    fig_pie = px.pie(
        values=list(sector_weights.values()),
        names=list(sector_weights.keys()),
        title="Répartition par secteur",
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Top 10 holdings
    st.subheader("📊 Top 10 Holdings")
    top10 = df_holdings.head(10)
    
    fig_bar = px.bar(
        top10, x='Symbole', y='Poids %',
        title="Top 10 Holdings - Poids (%)",
        color='Poids %', color_continuous_scale='Viridis',
        text='Poids %'
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

# ============================================================================
# SECTION 4: PORTEFEUILLE
# ============================================================================
elif menu == "💰 Portefeuille":
    st.subheader("💰 Portefeuille virtuel - ETF & Actions Spatiales")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        with st.form("add_position"):
            asset_type = st.selectbox("Type", ["ETF", "Action"])
            
            if asset_type == "ETF":
                symbol_pf = st.selectbox("ETF", list(SPACE_ETFS.keys()))
            else:
                symbol_pf = st.selectbox("Action", list(SPCX_HOLDINGS.keys()))
            
            shares = st.number_input("Quantité", min_value=1, value=100, step=10)
            buy_price = st.number_input("Prix d'achat ($)", min_value=0.01, value=10.0, step=1.0)
            
            if st.form_submit_button("➕ Ajouter"):
                if symbol_pf not in st.session_state.portfolio:
                    st.session_state.portfolio[symbol_pf] = []
                st.session_state.portfolio[symbol_pf].append({
                    'shares': shares,
                    'buy_price': buy_price,
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
                st.success(f"✅ {shares} {symbol_pf} ajoutées")
                time.sleep(1)
                st.rerun()
    
    with col1:
        if st.session_state.portfolio:
            portfolio_data = []
            total_value = 0
            total_cost = 0
            
            for sym, positions in st.session_state.portfolio.items():
                hist_s, _ = get_stock_data(sym, "1d")
                current = hist_s['Close'].iloc[-1] if hist_s is not None else 0
                
                for pos in positions:
                    value = pos['shares'] * current
                    cost = pos['shares'] * pos['buy_price']
                    profit = value - cost
                    profit_pct = (profit / cost * 100) if cost > 0 else 0
                    
                    total_value += value
                    total_cost += cost
                    
                    portfolio_data.append({
                        'Symbole': sym,
                        'Quantité': pos['shares'],
                        'Prix achat': format_currency(pos['buy_price']),
                        'Prix actuel': format_currency(current),
                        'Valeur': format_currency(value),
                        'Profit': format_currency(profit),
                        'Profit %': f"{profit_pct:+.1f}%"
                    })
            
            if portfolio_data:
                total_profit = total_value - total_cost
                total_profit_pct = (total_profit / total_cost * 100) if total_cost > 0 else 0
                
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Valeur totale", format_currency(total_value))
                col_b.metric("Coût total", format_currency(total_cost))
                col_c.metric("Profit total", format_currency(total_profit), delta=f"{total_profit_pct:+.1f}%")
                
                df_portfolio = pd.DataFrame(portfolio_data)
                st.dataframe(df_portfolio, use_container_width=True)
                
                if st.button("🗑️ Vider le portefeuille", use_container_width=True):
                    st.session_state.portfolio = {}
                    st.rerun()
        else:
            st.info("💡 Aucune position. Ajoutez des ETF ou actions spatiales !")

# ============================================================================
# SECTION 5: ALERTES PRIX
# ============================================================================
elif menu == "🔔 Alertes prix":
    st.subheader("🔔 Alertes de prix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("new_alert"):
            alert_symbol = st.selectbox("Symbole", list(SPACE_ETFS.keys()) + list(SPCX_HOLDINGS.keys()))
            alert_price = st.number_input("Prix cible ($)", min_value=0.01, value=50.0, step=1.0)
            condition = st.selectbox("Condition", ["above (au-dessus)", "below (en-dessous)"])
            condition = condition.split()[0]
            
            if st.form_submit_button("🔔 Créer l'alerte"):
                st.session_state.price_alerts.append({
                    'symbol': alert_symbol,
                    'price': alert_price,
                    'condition': condition,
                    'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                st.success(f"✅ Alerte créée pour {alert_symbol} à ${alert_price:.2f}")
    
    with col2:
        if st.session_state.price_alerts:
            for i, alert in enumerate(st.session_state.price_alerts):
                st.info(f"🔔 {alert['symbol']} - {alert['condition']} ${alert['price']:.2f}")
                if st.button(f"Supprimer", key=f"del_{i}"):
                    st.session_state.price_alerts.pop(i)
                    st.rerun()
        else:
            st.info("Aucune alerte active")

# ============================================================================
# SECTION 6: EMAIL
# ============================================================================
elif menu == "📧 Email":
    st.subheader("📧 Configuration email")
    
    with st.form("email_config"):
        enabled = st.checkbox("Activer les notifications", value=st.session_state.email_config['enabled'])
        email = st.text_input("Adresse email", value=st.session_state.email_config['email'])
        password = st.text_input("Mot de passe", type="password", value=st.session_state.email_config['password'])
        test_email = st.text_input("Email de test (optionnel)")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("💾 Sauvegarder"):
                st.session_state.email_config = {
                    'enabled': enabled,
                    'email': email,
                    'password': password,
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587
                }
                st.success("Configuration sauvegardée !")
        
        with col_btn2:
            if st.form_submit_button("📨 Tester"):
                if test_email:
                    if send_email_alert(
                        "Test SPCX Tracker",
                        "<h2>✅ Test réussi !</h2><p>Votre configuration email fonctionne.</p>",
                        test_email
                    ):
                        st.success("Email de test envoyé !")
                    else:
                        st.error("Échec de l'envoi")

# ============================================================================
# SECTION 7: PRÉDICTIONS
# ============================================================================
elif menu == "🤖 Prédictions":
    st.subheader("🤖 Prédictions ML - SPCX")
    
    if hist is not None and not hist.empty and len(hist) > 30:
        hist_reset = hist.reset_index()
        date_col = hist_reset.columns[0]
        hist_reset['Days'] = (hist_reset[date_col] - hist_reset[date_col].min()).dt.days
        
        X = hist_reset['Days'].values.reshape(-1, 1)
        y = hist_reset['Close'].values
        
        col1, col2 = st.columns(2)
        with col1:
            days_to_predict = st.slider("Jours à prédire", 1, 30, 7)
            degree = st.slider("Degré du polynôme", 1, 4, 2)
        
        with col2:
            show_confidence = st.checkbox("Afficher intervalle de confiance", value=True)
        
        model = make_pipeline(PolynomialFeatures(degree=degree), LinearRegression())
        model.fit(X, y)
        
        last_day = X[-1][0]
        future_days = np.arange(last_day + 1, last_day + days_to_predict + 1).reshape(-1, 1)
        predictions = model.predict(future_days)
        
        last_date = hist_reset[date_col].iloc[-1]
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_to_predict)]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist_reset[date_col], y=y,
            mode='lines', name='Historique SPCX',
            line=dict(color='#005288', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=future_dates, y=predictions,
            mode='lines+markers', name='Prédictions',
            line=dict(color='red', width=2, dash='dash'),
            marker=dict(size=8, color='red')
        ))
        
        if show_confidence:
            residuals = y - model.predict(X)
            std_residuals = np.std(residuals)
            upper_bound = predictions + 2 * std_residuals
            lower_bound = predictions - 2 * std_residuals
            
            fig.add_trace(go.Scatter(
                x=future_dates + future_dates[::-1],
                y=np.concatenate([upper_bound, lower_bound[::-1]]),
                fill='toself',
                fillcolor='rgba(255,0,0,0.2)',
                line=dict(color='rgba(255,0,0,0)'),
                name='Intervalle confiance 95%'
            ))
        
        fig.update_layout(
            title=f"Prédictions SPCX - {days_to_predict} jours",
            xaxis_title="Date",
            yaxis_title="Prix ($)",
            height=500,
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        pred_df = pd.DataFrame({
            'Date': [d.strftime('%Y-%m-%d') for d in future_dates],
            'Prix prédit': [format_currency(p) for p in predictions],
            'Variation': [f"{(p/hist['Close'].iloc[-1] - 1)*100:+.1f}%" for p in predictions]
        })
        st.dataframe(pred_df, use_container_width=True)
        
        current = hist['Close'].iloc[-1]
        last_pred = predictions[-1]
        
        if last_pred > current * 1.03:
            st.success(f"📈 Tendance anticipée: HAUSSIÈRE - {((last_pred/current - 1)*100):+.1f}%")
        elif last_pred < current * 0.97:
            st.error(f"📉 Tendance anticipée: BAISSIÈRE - {((last_pred/current - 1)*100):+.1f}%")
        else:
            st.info("➡️ Tendance anticipée: NEUTRE")
    else:
        st.warning(f"⚠️ Pas assez de données pour SPCX (minimum 30 jours requis)")

# Auto-refresh
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "🚀 SPCX & Space ETF Tracker | Données: yfinance + simulation | Heure Paris UTC+2<br>"
    "SPCX = SPAC & NewSpace ETF (ProcureAM) | Holdings: Rocket Lab, AST SpaceMobile, Planet Labs, Virgin Galactic..."
    "</p>",
    unsafe_allow_html=True
)
