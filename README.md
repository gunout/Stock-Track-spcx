<div align="center">

# 🚀 SPCX & Space ETF Tracker

**Dashboard Streamlit de suivi des ETF spatiaux et actions NewSpace — Analyse temps réel & IA**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![yfinance](https://img.shields.io/badge/yfinance-Market%20Data-00B386?style=for-the-badge&logo=yahoo&logoColor=white)](https://github.com/ranaroussi/yfinance)
[![License: MIT](https://img.shields.io/badge/License-MIT-000091?style=for-the-badge&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Actif-00d4ff?style=for-the-badge&logo=statuspage&logoColor=white)](#)
[![PRs Welcome](https://img.shields.io/badge/PRs-Bienvenues-ff69b4?style=for-the-badge&logo=git&logoColor=white)](#-contribuer)

**📊 Suivi SPCX • 🏆 Comparatif ETF • 🤖 Prédictions IA • 💰 Portefeuille virtuel**

</div>

---

## 📖 Sommaire

- [Aperçu](#-aperçu)
- [Fonctionnalités](#-fonctionnalités)
- [Sections du dashboard](#-sections-du-dashboard)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [ETF spatiaux couverts](#-etf-spatiaux-couverts)
- [Holdings SPCX](#-holdings-spcx)
- [Prédictions IA](#-prédictions-ia)
- [Alertes & Email](#-alertes--email)
- [Structure du projet](#-structure-du-projet)
- [Limitations](#-limitations)
- [Contribuer](#-contribuer)
- [Licence](#-licence)

---

## 🎯 Aperçu

**SPCX & Space ETF Tracker** est une application **Streamlit** de surveillance des ETF spatiaux et actions **NewSpace**. Elle permet de :

- 📊 Suivre le **SPCX** (SPAC & NewSpace ETF de ProcureAM) en temps réel
- 🏆 Comparer les **6 principaux ETF spatiaux** (SPCX, UFO, ARKX, ROKT, ITA, PPA)
- 🚀 Analyser les **12 principales holdings** du SPCX (Rocket Lab, AST SpaceMobile, Planet Labs...)
- 🤖 Générer des **prédictions IA** via régression polynomiale
- 💰 Simuler un **portefeuille virtuel** avec calcul de profits
- 🔔 Configurer des **alertes de prix** personnalisées
- 📧 Recevoir des **notifications par email**

Le tout dans une interface moderne avec **graphiques interactifs Plotly**, **fallback automatique** en cas d'absence de données, et **fuseaux horaires Paris/New York**.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---|---|
| 📈 **Dashboard SPCX** | Prix temps réel, MA20, MA50, volatilité, performance |
| 🏆 **Comparatif ETF** | Score algorithmique (AUM, frais, holdings, perf) |
| 📊 **Holdings SPCX** | Top 10, répartition sectorielle, prix temps réel |
| 💰 **Portefeuille** | Ajout de positions, calcul profits/P&L, valeur totale |
| 🔔 **Alertes prix** | Alertes au-dessus/en-dessous d'un seuil |
| 📧 **Email** | Configuration SMTP + notifications automatiques |
| 🤖 **Prédictions IA** | Régression polynomiale (degré 1-4) + intervalle de confiance |
| 🕐 **Fuseaux horaires** | Paris (UTC+2) et New York (UTC-4/-5) |
| 🔄 **Auto-refresh** | Rafraîchissement automatique configurable (5-60s) |
| 💾 **Fallback intelligent** | Données simulées si yfinance échoue |
| 📊 **Graphiques Plotly** | Interactifs, zoomables, exportables |
| 📱 **Responsive** | Interface adaptée à tous les écrans |

---

## 📋 Sections du dashboard

### 1️⃣ 📈 SPCX Dashboard
- Prix en temps réel + variation
- Graphique candlestick avec MA20/MA50
- Volatilité annualisée
- Performance sur la période
- Top 5 holdings avec prix
- Comparaison vs UFO, ARKX, ITA

### 2️⃣ 🏆 Comparatif ETF
- Score algorithmique sur 100 points
- Grade : EXCELLENT / TRÈS BON / BON / FAIBLE
- AUM, frais, nombre de holdings
- Graphique comparatif multi-ETF

### 3️⃣ 📊 Holdings SPCX
- Liste complète des 12 holdings
- Poids, secteur, valeur estimée
- Répartition sectorielle (pie chart)
- Top 10 en bar chart

### 4️⃣ 💰 Portefeuille
- Ajout de positions (ETF + actions)
- Calcul P&L en temps réel
- Valeur totale, coût, profit
- Suppression / vidage complet

### 5️⃣ 🔔 Alertes prix
- Création d'alertes (above/below)
- Liste des alertes actives
- Suppression individuelle

### 6️⃣ 📧 Email
- Configuration SMTP (Gmail compatible)
- Test d'envoi
- Notifications automatiques

### 7️⃣ 🤖 Prédictions
- Régression polynomiale ajustable
- Intervalle de confiance 95%
- Prévision jusqu'à 30 jours
- Tendance HAUSSIÈRE / BAISSIÈRE / NEUTRE

---

## 🚀 Installation

### Prérequis

- **Python 3.10+**
- pip / virtualenv

### Cloner le projet

```bash
git clone https://github.com/gunout/spcx-space-tracker.git
cd spcx-space-tracker
```

### Environnement virtuel

```bash
python3 -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

**Ou manuellement :**

```bash
pip install streamlit yfinance pandas numpy plotly scikit-learn pytz
```

---

## ▶️ Utilisation

### Lancer l'application

```bash
streamlit run app.py
```

L'application s'ouvre automatiquement à l'adresse :

```
🌐 http://localhost:8501
```

### Navigation

Utilise la **sidebar** à gauche pour naviguer entre les sections :

- 📈 SPCX Dashboard
- 🏆 Comparatif ETF
- 📊 Holdings SPCX
- 💰 Portefeuille
- 🔔 Alertes prix
- 📧 Email
- 🤖 Prédictions

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    STREAMLIT APP (Client)                  │
│                                                            │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│   │  Dashboard   │  │  Comparatif  │  │  Prédictions │    │
│   │    SPCX      │  │     ETF      │  │      IA      │    │
│   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│          │                 │                 │            │
│          └─────────────────┼─────────────────┘            │
│                            ▼                              │
│              ┌──────────────────────────┐                 │
│              │   get_stock_data()       │                 │
│              │   calculate_etf_score()  │                 │
│              └──────────┬───────────────┘                 │
└─────────────────────────┼─────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
     ┌─────────────────┐     ┌──────────────────┐
     │   yfinance      │     │  Fallback Data   │
     │  (temps réel)   │     │   (simulation)   │
     │   CORS ✅       │     │   local ✅       │
     └─────────────────┘     └──────────────────┘
```

**Fonctionnement** :
1. Streamlit interroge `yfinance` pour obtenir les données de marché
2. Si l'API échoue, un **fallback local** génère des données réalistes
3. Un **cache de 5 minutes** évite les appels répétés
4. Les prédictions IA utilisent **scikit-learn** (régression polynomiale)

---

## 📊 ETF spatiaux couverts

| ETF | Nom | AUM | Frais | Holdings |
|-----|-----|-----|-------|----------|
| **SPCX** | SPAC & NewSpace ETF | $125M | 0.75% | 25 |
| **UFO** | Procure Space ETF | $180M | 0.75% | 30 |
| **ARKX** | ARK Space Exploration ETF | $350M | 0.75% | 40 |
| **ROKT** | SPDR S&P Aerospace & Defense | $800M | 0.35% | 45 |
| **ITA** | iShares US Aerospace & Defense | $5.2B | 0.40% | 38 |
| **PPA** | Invesco Aerospace & Defense | $2.1B | 0.56% | 50 |

---

## 🚀 Holdings SPCX

Le SPCX investit dans **12 sociétés NewSpace** :

| Symbole | Société | Secteur | Poids |
|---------|---------|---------|-------|
| **RKLB** | Rocket Lab USA | Lanceurs | 12.5% |
| **ASTS** | AST SpaceMobile | Satellites | 8.2% |
| **PL** | Planet Labs | Imagerie | 7.5% |
| **RDW** | Redwire | Infrastructure | 6.8% |
| **IRDM** | Iridium | Communications | 6.2% |
| **SPCE** | Virgin Galactic | Tourisme | 5.2% |
| **GSAT** | Globalstar | Communications | 4.8% |
| **LLAP** | Terran Orbital | Satellites | 3.5% |
| **BKSY** | BlackSky | Imagerie | 3.2% |
| **SATL** | Satellogic | Imagerie | 2.8% |
| **ASTR** | Astra Space | Lanceurs | 2.5% |
| **MNTS** | Momentus | Logistique | 1.8% |

---

## 🤖 Prédictions IA

Le module de prédiction utilise **scikit-learn** :

- **Modèle** : Régression polynomiale (`PolynomialFeatures` + `LinearRegression`)
- **Degré ajustable** : 1 à 4
- **Horizon** : 1 à 30 jours
- **Intervalle de confiance** : 95% (basé sur les résidus)

**Exemple de sortie** :

```
📈 Tendance anticipée: HAUSSIÈRE +5.2%
```

---

## 🔔 Alertes & Email

### Alertes prix
- **Condition** : `above` (au-dessus) ou `below` (en-dessous)
- **Cible** : n'importe quel ETF ou action du portefeuille
- **Stockage** : `st.session_state.price_alerts`

### Email (SMTP)
- **Serveur** : Gmail (`smtp.gmail.com:587`)
- **Auth** : Email + mot de passe d'application
- **Utilisation** : Notifications automatiques + test

> ⚠️ **Sécurité** : N'utilise pas ton mot de passe principal Gmail. Crée un **mot de passe d'application** dans ton compte Google.

---

## 📂 Structure du projet

```
spcx-space-tracker/
├── app.py                    # Application Streamlit principale
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
├── LICENSE                   # Licence MIT
└── .gitignore                # Fichiers exclus
```

### Dépendances principales

| Librairie | Version | Usage |
|-----------|---------|-------|
| streamlit | 1.30+ | Interface web |
| yfinance | 0.2+ | Données de marché |
| pandas | 2.0+ | Manipulation de données |
| numpy | 1.24+ | Calcul scientifique |
| plotly | 5.0+ | Graphiques interactifs |
| scikit-learn | 1.3+ | Prédictions IA |
| pytz | 2023+ | Fuseaux horaires |

---

## ⚠️ Limitations

| Limitation | Cause | Impact |
|---|---|---|
| **Données yfinance** | Rate-limit Yahoo | Fallback automatique |
| **SPCX peu liquide** | ETF récent (2021) | Données parfois manquantes |
| **Prédictions IA** | Régression polynomiale simple | Pas de deep learning |
| **Email Gmail** | Nécessite mot de passe d'app | Configuration manuelle |
| **Auto-refresh** | Streamlit = pas temps réel | Refresh manuel ou auto |

> Ce tracker est un **outil d'analyse** et **ne constitue pas un conseil en investissement**. Les performances passées ne préjugent pas des performances futures.

---

## 🤝 Contribuer

Les contributions sont **bienvenues** !

1. **Forkez** le projet
2. **Créez** une branche (`git checkout -b feature/amelioration`)
3. **Committez** vos changements (`git commit -m "Ajout: nouvelle fonctionnalité"`)
4. **Poussez** la branche (`git push origin feature/amelioration`)
5. **Ouvrez** une Pull Request

### Idées d'améliorations

- [ ] Intégrer l'API Alpha Vantage ou Polygon pour des données plus fiables
- [ ] Ajouter un modèle LSTM pour les prédictions
- [ ] Implémenter un backtesting des stratégies
- [ ] Ajouter un mode sombre
- [ ] Support multilingue (EN/FR)
- [ ] Export PDF des rapports
- [ ] Notifications Telegram/Discord
- [ ] Comparaison avec le secteur aérospatial global

---

 ### LIENS APPLICATION STREAMLIT EN LIGNE :

    https://stock-track-spcx.streamlit.app/
---

## 📄 Licence

Ce projet est sous **licence MIT** — voir [LICENSE](LICENSE).

```
MIT License

Copyright (c) 2026 SPCX & Space ETF Tracker

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**🚀 SPCX & Space ETF Tracker**

*Dashboard Streamlit de suivi des ETF spatiaux*

[![GitHub Stars](https://img.shields.io/github/stars/gunout/spcx-space-tracker?style=social)](https://github.com/gunout/spcx-space-tracker)
[![GitHub Forks](https://img.shields.io/github/forks/gunout/spcx-space-tracker?style=social)](https://github.com/gunout/spcx-space-tracker)
[![GitHub Issues](https://img.shields.io/github/issues/gunout/spcx-space-tracker?style=social)](https://github.com/gunout/spcx-space-tracker/issues)

**Fait avec Python — © 2026**

</div>

---

<div align="center">

### 🇪🇺 Gunout · 2026

![Made in France](https://img.shields.io/badge/Made_in-France-002395?style=flat-square&labelColor=FFFFFF&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MDAgNjAwIj48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjYwMCIgZmlsbD0iIzAwMjM5NSIvPjxyZWN0IHdpZHRoPSI5MDAiIGhlaWdodD0iNDAwIiB5PSIxMDAiIGZpbGw9IiNmZmYiLz48cmVjdCB3aWR0aD0iOTAwIiBoZWlnaHQ9IjIwMCIgeT0iNDAwIiBmaWxsPSIjZWQyOTM5Ii8+PC9zdmc+)
![GitHub](https://img.shields.io/badge/GitHub-gunout-181717?style=flat-square&logo=github&logoColor=white)
![Year](https://img.shields.io/badge/2026-ED2939?style=flat-square&labelColor=FFFFFF)

<sub>© 2026 <strong>Gunout</strong> — Tous droits réservés.</sub>

</div>
