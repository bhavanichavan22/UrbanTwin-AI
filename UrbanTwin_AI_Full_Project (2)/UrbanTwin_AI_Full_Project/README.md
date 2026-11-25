# UrbanTwin AI – Smart City Scenario Simulator
**Tagline:** Simulate Today. Shape Tomorrow.

An MCA-friendly full-stack academic prototype using Python, Streamlit, Pandas, NumPy, Plotly, SQLite, ReportLab and optional Gemini LLM integration.

## Features
- Smart City dashboard with latest saved scenario indicators and activity charts.
- Traffic congestion simulation: vehicle demand, road capacity, population density, public transport, smart signals, road expansion and carpooling.
- Water shortage simulation: demand, supply, reservoir availability, population, consumption, conservation, rainwater harvesting and leakage reduction.
- Waste accumulation simulation: generation, collection capacity, population, recycling, segregation, collection efficiency and composting.
- Before/after scenario metrics and Plotly charts.
- AI scenario analysis with Gemini API, plus a local fallback if no key or API service is unavailable.
- Rule-based recommendation engine with reasons.
- SQLite scenario history: save, view, delete and compare.
- Downloadable PDF report for each scenario.

## 1. Extract the ZIP
Extract `UrbanTwin_AI_Full_Project.zip` to a folder such as `C:\MCA\UrbanTwin_AI_Full_Project`.

## 2. Open in VS Code
Open Visual Studio Code → File → Open Folder → select the extracted project folder. Open Terminal → New Terminal.

## 3. Create a virtual environment
Windows:
```powershell
py -m venv .venv
.venv\Scripts\activate
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Gemini API (optional)
Copy `.env.example` to `.env`. Add your key:
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```
The application works without an API key using local fallback recommendations. Never share or commit your API key.

## 6. Run the application
```bash
streamlit run app.py
```
Open the local URL shown in the terminal, usually `http://localhost:8501`.

## 7. Run tests
```bash
pytest -q
```

## Project structure
```text
UrbanTwin_AI_Full_Project/
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── urbantwin.db             # created automatically on first run
├── urbantwin/
│   ├── __init__.py
│   ├── simulation.py
│   ├── ai_engine.py
│   ├── recommendations.py
│   ├── database.py
│   └── report.py
├── data/
│   └── sample_city_data.csv
├── reports/
├── tests/
│   └── test_simulation.py
└── .streamlit/
    └── config.toml
```

## Architecture
1. Streamlit UI collects user-selected scenario parameters.
2. Simulation module computes baseline and intervention indicators.
3. Recommendation engine maps scenario metrics to prioritised actions.
4. Optional Gemini LLM receives the exact input and calculated result to generate explanations; numerical claims must come from application data.
5. SQLite stores scenario name, category, parameters, results, recommendations and timestamp.
6. ReportLab generates a PDF scenario report for download.

## Academic assumptions and limitations
This is a digital-twin-inspired prototype, not a production digital twin. The equations are intentionally simplified and use hypothetical inputs. The application does not connect to live traffic sensors, municipal water telemetry, GIS, or waste collection services. LLM output may be incomplete or inaccurate. Validate with city datasets and domain experts before real-world decisions.

## Viva preparation: explain the project in one minute
“UrbanTwin AI is a Python and Streamlit-based smart-city scenario simulator. It models traffic congestion, water shortage and waste accumulation. Users adjust parameters and interventions, and the simulation module calculates baseline and projected indicators. Plotly visualises the results, SQLite stores scenario history, and a recommendation engine suggests actions. An optional Gemini LLM explains the scenario using the calculated values. If the API key is unavailable, local fallback recommendations keep the application functional. Users can compare saved scenarios and download PDF reports.”
