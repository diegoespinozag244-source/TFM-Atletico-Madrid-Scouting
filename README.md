# TFM · Data-Driven Sporting Direction & Scouting — Atlético de Madrid 26/27

End-to-end data science pipeline for football recruitment decisions: from raw event data to validated statistical models, a player-similarity recommendation engine, and financial feasibility analysis — packaged as an interactive Streamlit application.

**MSc Thesis · Big Data Analysis & Sports Scouting** · Real Madrid Graduate School / Universidad Europea · 2025/26
**Author:** Diego Espinoza González — [diegoespinozag244@gmail.com](mailto:diegoespinozag244@gmail.com)

---

## Overview

The project answers a single question: *how should Atlético de Madrid rebuild its squad for 26/27 in a way that is both tactically coherent and financially viable?*

It does this through a fully reproducible, five-stage pipeline built entirely on real data — no missing field is invented or approximated.

```
ETL  →  Playing-style model  →  Squad SWOT  →  Scouting engine  →  Financial validation
```

The final deliverable is a **7-section interactive Streamlit app** that takes a user from the club's tactical identity to a concrete, budget-constrained list of transfer targets.

## Data

- **Opta event data** — 3,358 players across Europe's five major leagues (LaLiga, Premier League, Serie A, Bundesliga, Ligue 1)
- **Capology** — real salary data, used for wage-bill and Fair Play analysis
- **Reliability filter**: only players with ≥450 minutes played are used in comparative analysis, to reduce small-sample noise
- **Transparency principle**: the dataset does not include age, height, preferred foot, market value or contract expiry. These are never inferred — where used (e.g. player age), the value is sourced from an external reference (Transfermarkt / Capology) and clearly labelled as such, never treated as part of the core dataset

## Methodology

1. **ETL & cleaning** (`pandas`) — ingestion and normalization of the Opta dataset into position-based KPI tables
2. **Playing-style model** — percentile ranking of Atlético's 25/26 KPIs against the full league, producing a radar profile that defines the club's tactical identity and, by extension, the ideal statistical profile per position
3. **Squad audit (SWOT)** — performance-by-position analysis (e.g. goals/90 vs. passes/90) to diagnose finishing dependency, ageing key positions and recruitment needs
4. **Scouting engine** — each of the 3,358 players is vectorised on position-specific KPIs and scored for similarity against Atlético's target profile per position; results are cross-checked against real transfer constraints (buy-back clauses, sell-on percentages)
5. **Financial validation** — every recommended transfer is checked against the club's real wage bill, projected savings and La Liga / UEFA Fair Play limits

## Key results

- 4 concrete recruitment targets identified (forward, midfielder, centre-back, goalkeeper), each benchmarked against the player they would replace
- Full operation (3 field-player signings, ~€73M) **reduces** the wage bill by an estimated €12.2M/year while remaining Fair Play compliant
- Strategic scenario analysis on a high-value sale (Julián Álvarez) modelling the trade-off between transfer funds and lost goal output

## The application

Built with **Streamlit** + **Plotly**, structured in 7 navigable sections:

| Section | Content |
|---|---|
| Playing Style | KPI radar and percentile ranking vs. league |
| Squad Audit | Performance-by-position visual diagnostic |
| Individual Analysis | Player card, pitch map, dominance profile |
| Scouting Engine | Similarity search across 5 leagues |
| Comparator | Overlay radar for up to 4 players |
| Recruitment Targets | Target vs. incumbent radar comparison |
| Financial Analysis | Wage bill, net spend, Fair Play compliance |

## Tech stack

`Python` · `pandas` · `Plotly` · `Streamlit`

## Repository structure

```
app.py                      # Streamlit application (entry point)
master_5_ligas.csv          # Full 5-league player dataset (Opta)
master_jugadores.csv        # Processed player master table
modelo_juego_laliga.csv     # LaLiga playing-style benchmark data
plantilla_salarios.csv      # Squad + salary data (Capology)
scouting_candidatos.csv     # Scouting engine candidate pool
fichajes_objetivo.csv       # Final recruitment targets output
fichajes_financiero.csv     # Financial validation output
requirements.txt            # Python dependencies
```

## Running locally

```bash
git clone https://github.com/diegoespinozag244-source/TFM-Atletico-Madrid-Scouting.git
cd TFM-Atletico-Madrid-Scouting
pip install -r requirements.txt
streamlit run app.py
```

## Limitations & future work

- No physical/GPS tracking data — the model relies on event data only
- Planned extensions: incorporate tracking data, player valuation modelling, and age-based performance projection

---

*This project was developed as the final thesis for the MSc in Big Data Analysis & Sports Scouting at Real Madrid Graduate School / Universidad Europea (2025/26).*
