# Magnus Carlsen Performance Analysis

An end-to-end data analysis project exploring 9,336 of Magnus Carlsen's games on Chess.com (2014–2026), fetched via the public Chess.com API. The project investigates his opening performance, in-session fatigue, tilt after losses, and resilience under pressure — moving from raw API data through cleaning, exploratory analysis, predictive modeling, and an interactive dashboard.

## Why this project

I picked this project because it sits at the intersection of two things I'm genuinely interested in: chess and data science. Instead of working with a generic dataset, I wanted to apply what I was learning to something I actually cared about following and understanding.

## Project status

- ✅ Data fetching — Python script pulling full game archives via the Chess.com public API
- ✅ Data cleaning — handling missing values, simplifying categories, feature engineering
- ✅ Exploratory data analysis — 10 analytical questions answered with visualizations
- ✅ Predictive modeling — RandomForestRegressor predicting next-game accuracy, with leakage-safe time-series cross-validation
- ✅ Interactive dashboard — Power BI, 4-page report built on top of the EDA findings (demo video linked below)

## Key findings

- Clean games (both players ≥93.84% accuracy) skew heavily toward draws (81.6%), while messy games are far more decisive — and within decisive outcomes, Magnus's win:loss ratio is actually slightly better in messy games (2.3:1) than clean ones (1.9:1).
- His most-played openings are the Sicilian Defense, King's Indian, and English Opening, with win rates ranging 68–73.5% across his top 6.
- Accuracy decays measurably within a session: across roughly 25 games played back-to-back, average accuracy drifts down from ~90% to ~88%, a visible if modest fatigue effect (see dashboard, Session & Formats page).
- Rapid is Magnus's best format by accuracy (~93%), ahead of blitz and bullet (~88–90%), but blitz edges out rapid on win rate — he trades some precision for results as time control tightens.
- On a composite rating balancing win rate, safety, accuracy, consistency, and frequency, King's Indian is Magnus's strongest opening by a wide margin (9,217 pts), with Queens Gambit (5,813) and English Opening (5,631) as a clear second tier.
- Despite this pattern surfacing clearly in EDA, it did *not* translate into a useful predictive signal — see modeling results below.

## Dashboard

An interactive 4-page Power BI dashboard, directly derived from the EDA notebook's findings — each page takes a pattern discovered during exploratory analysis and makes it interactively explorable:

1. **Macro Trends** — Magnus's rating and win-rate trajectory from 2014–2026 across standard chess and chess960, plus a game-count breakdown by variant and time control.
2. **Session & Formats** — accuracy trends over time, a format comparison (accuracy vs. win rate across bullet/blitz/rapid), and the session fatigue curve: accuracy decaying as game number within a session increases. This is the page I find most interesting — it's the same fatigue signal the ML notebook later tried, and failed, to turn into a predictive feature (see below).
3. **Opening Strategy** — volume vs. win rate across Magnus's top 6 openings, plus a risk/precision matrix plotting loss rate against accuracy per opening, sized by game volume.
4. **Opening Radars** — a master radar comparing composite ratings across all six openings, with a drill-down radar (win rate, safety, accuracy, consistency, frequency) for any opening selected from the grid.

**Dashboard + demo video:** [Google Drive folder](https://drive.google.com/drive/folders/1ZHUz3stToEKvg4-I9NaMEgGc4-MSdQ6n)

## Predictive modeling

A RandomForestRegressor trained to predict Magnus's accuracy in his *next* game within a session, using pre-game and post-game context (ratings, time control, session position, rolling accuracy, etc.) as features, with the target computed via `groupby('session_id').shift(-1)` and evaluated with `TimeSeriesSplit` to avoid any leakage across time.

**What the model found.** The final model explains a modest but real amount of variance in next-game accuracy (test R² ≈ 0.055) — roughly 5.5% of the variation, meaning its predictions are only slightly better than guessing Magnus's average accuracy every time. The hyperparameter search reinforces this: the best model settled on `max_depth=2`, an almost trivially shallow tree, and allowing deeper trees (`max_depth=None`) made cross-validated error *worse* — the algorithm wasn't finding deeper patterns, it was fitting noise.

Comparing impurity-based and permutation importance was informative in its own right. Impurity importance initially suggested `opponent_rating` was a major driver, but permutation importance — which measures the actual drop in test performance when a feature is shuffled — showed this was misleading; shuffling `opponent_rating` barely moves prediction error. The feature that holds up under both methods is `time_since_last_game_min`, with `base_time_seconds` a distant but real second. Every other feature — including the ones the original fatigue hypothesis was built around (`game_number_in_session`, `rolling_avg_accuracy_last5`) — contributed negligibly once measured correctly.

**Why this result makes sense.** This result isn't a failure of the model or the feature engineering — it's consistent with what the dataset can and can't represent. A chess game's accuracy is decided move by move, inside the game: the specific position reached, whether a tactic was missed or found, how sharp or simplified the position became, how much the opponent's choices forced difficult decisions. None of that lives in this dataset. What this dataset holds is *post-game and pre-game context* — ratings, time formats, outcomes, timestamps — a layer that sits entirely outside the game itself.

Put directly: predicting an in-game outcome (accuracy) from pre-game and post-game metadata means asking context about a game to substitute for content within it. Context can set the conditions a game is played under, but it can't see the moves. A session-fatigue signal might nudge the odds of a mistake, but it can't tell you whether that mistake actually got made, missed, or punished in this specific game — that depends on what's on the board.

Seen this way, the weak R² isn't an open question so much as an expected outcome, now confirmed rather than assumed: this feature set was always structurally one level removed from what actually determines the target. Notably, the dashboard's session fatigue chart shows the *aggregate* pattern clearly — accuracy does trend down across a session, on average — but that population-level trend doesn't carry enough signal to predict any single next game, which is exactly what the permutation importance results confirm.

**Where real signal would have to come from.** Closing this gap would likely require in-game features this dataset doesn't contain — engine evaluation swings move by move, time spent per move, how sharp or forcing the position was, or move-level complexity. Those require PGN-level analysis, not just game metadata, and are a natural direction for a follow-up notebook rather than further tuning of this one. Further grid search or feature engineering within the current feature set is unlikely to move this result meaningfully — the ceiling here is the data available, not the model.


## Repository structure

```
magnus-carlsen-performance-analysis/
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   ├── magnus_games.csv                  # Raw data from Chess.com API
│   ├── magnus_cleaned_games.csv          # Cleaned, full dataset (incl. chess960 etc.)
│   └── magnus_cleaned_chess_games.csv    # Cleaned, standard chess only
├── notebooks/
│   ├── DATA-CLEANING.ipynb
│   ├── EDA.ipynb
│   └── ML-PREDICTION.ipynb
├── scripts/
│   └── fetch_games.py                    # Chess.com API fetch script
└── requirements.txt
```


Dashboard demo video are hosted on Google Drive — see link above.

## Dataset

- **Source:** [Chess.com Published-Data API](https://www.chess.com/news/view/published-data-api) (public, no auth required)
- **Scope:** All of Magnus Carlsen's available games, December 2014 – May 2026
- **Size:** 9,336 games, 21 raw columns, expanded with engineered features during cleaning
- **Game types:** Standard chess, Chess960, three-check, and odds chess (standard chess isolated for most analyses — see cleaning notebook for rationale)

## Methodology

1. **Fetching** — Games pulled from the Chess.com API with retry logic, saved as JSON, converted to CSV.
2. **Cleaning** — Duplicate checks, missing value handling (documented per-column, not blanket-dropped), timestamp conversion, outcome simplification (win/loss/draw), opening name simplification, game-type classification (clean/messy/mixed via accuracy quantiles), rating outlier filtering, session/fatigue detection (30-minute gap rule), and upset detection (90th-percentile rating-gap threshold on losses). Every cleaning decision is explained inline in the notebook, not just applied silently.
3. **EDA** — 10 structured questions covering accuracy vs. outcome, tilt after losses, in-session fatigue, opening safety/risk, time-format performance, and year-over-year trends — each scoped to the correct dataset (full vs. standard-chess-only) depending on whether the question needs full chronological continuity.
4. **Prediction** — A RandomForestRegressor predicting Magnus's accuracy in his *next* game within a session, trained with leakage-safe TimeSeriesSplit cross-validation and validated with both impurity and permutation feature importance (see Predictive modeling above for results).
5. **Dashboard** — An interactive 4-page Power BI dashboard built on top of the EDA findings, covering macro trends, session/format breakdowns, opening strategy, and composite opening ratings.

## Tech stack

- **Language:** Python 3.13
- **Core libraries:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Modeling:** scikit-learn (RandomForestRegressor, Pipeline, ColumnTransformer, TimeSeriesSplit)
- **Dashboard:** Power BI

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

- https://linkedin.com/in/priyanshverma1
