# Magnus Carlsen Performance Analysis

An end-to-end data analysis project exploring 9,336 of Magnus Carlsen's games on Chess.com (2014–2026), fetched via the public Chess.com API. The project investigates his opening performance, in-session fatigue, tilt after losses, and resilience under pressure — moving from raw API data through cleaning, exploratory analysis, and (in progress) predictive modeling.

## Why this project

I picked this project because it sits at the intersection of two things I'm genuinely interested in: chess and data science. Instead of working with a generic dataset, I wanted to apply what I was learning to something I actually cared about following and understanding.

## Project status

- ✅ Data fetching — Python script pulling full game archives via the Chess.com public API
- ✅ Data cleaning — handling missing values, simplifying categories, feature engineering
- ✅ Exploratory data analysis — 10 analytical questions answered with visualizations
- 🔄 Predictive modeling — RandomForestRegressor predicting next-game accuracy (in progress)
- 🔄 Interactive dashboard — Power BI / Tableau (in progress)

This repo is being actively built — check back for updates, or follow along via the commit history.

## Key findings so far

- Clean games (both players ≥93.84% accuracy) skew heavily toward draws (81.6%), while messy games are far more decisive — and within decisive outcomes, Magnus's win:loss ratio is actually slightly better in messy games (2.3:1) than clean ones (1.9:1).
- His most-played openings are the Sicilian Defense, King's Indian, and English Opening, with win rates ranging 68–73.5% across his top 6.
- [Add another 1–2 findings here as they firm up — e.g. anything from the fatigue/session or tilt questions once those are finalized]

## Repository structure

```
magnus-carlsen-performance-analysis/
├── README.md
├── data/
│   ├── magnus_games.csv                  # Raw data from Chess.com API
│   ├── magnus_cleaned_games.csv          # Cleaned, full dataset (incl. chess960 etc.)
│   └── magnus_cleaned_chess_games.csv    # Cleaned, standard chess only
├── notebooks/
│   ├── DATA-CLEANING.ipynb
│   ├── EDA.ipynb
│   └── ML-PREDICTION.ipynb               # In progress
├── scripts/
│   └── fetch_games.py                    # Chess.com API fetch script
├── dashboard/                            # Power BI / Tableau file (in progress)
└── requirements.txt
```

## Dataset

- **Source:** [Chess.com Published-Data API](https://www.chess.com/news/view/published-data-api) (public, no auth required)
- **Scope:** All of Magnus Carlsen's available games, December 2014 – May 2026
- **Size:** 9,336 games, 21 raw columns, expanded with engineered features during cleaning
- **Game types:** Standard chess, Chess960, three-check, and odds chess (standard chess isolated for most analyses — see cleaning notebook for rationale)

## Methodology

1. **Fetching** — Games pulled from the Chess.com API with retry logic, saved as JSON, converted to CSV.
2. **Cleaning** — Duplicate checks, missing value handling (documented per-column, not blanket-dropped), timestamp conversion, outcome simplification (win/loss/draw), opening name simplification, game-type classification (clean/messy/mixed via accuracy quantiles), rating outlier filtering, session/fatigue detection (30-minute gap rule), and upset detection (90th-percentile rating-gap threshold on losses). Every cleaning decision is explained inline in the notebook, not just applied silently.
3. **EDA** — 10 structured questions covering accuracy vs. outcome, tilt after losses, in-session fatigue, opening safety/risk, time-format performance, and year-over-year trends — each scoped to the correct dataset (full vs. standard-chess-only) depending on whether the question needs full chronological continuity.
4. **Prediction (in progress)** — A RandomForestRegressor predicting Magnus's accuracy in his *next* game within a session, based on a within-session accuracy decay pattern discovered during EDA.
5. **Dashboard (in progress)** — An interactive Power BI (or Tableau) dashboard for exploring the cleaned dataset.

## Tech stack

- **Language:** Python 3.13
- **Core libraries:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Modeling (in progress):** scikit-learn
- **Dashboard (in progress):** Power BI or Tableau

## Running this project locally

```bash
git clone https://github.com/<your-username>/magnus-carlsen-performance-analysis.git
cd magnus-carlsen-performance-analysis
pip install -r requirements.txt
jupyter notebook
```

Open the notebooks in order: `DATA-CLEANING.ipynb` → `EDA.ipynb` → `ML-PREDICTION.ipynb`.

## Author

Priyansh Verma

- LinkedIn: in/priyanshverma1
