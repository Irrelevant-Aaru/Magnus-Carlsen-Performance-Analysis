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
