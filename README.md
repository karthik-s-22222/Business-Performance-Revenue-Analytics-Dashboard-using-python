# Business Performance & Revenue Analytics Dashboard

An interactive, high-fidelity administrative analytics engine designed to track end-to-end customer lifecycles—spanning anonymous incoming leads, quote valuations, deal progress status loops, and liquid collection runways. 
---
## 🚀 Architectural Overview
This system functions entirely as a **frontend-driven, serverless single-page analytics application**. It simulates complex CRM and ERP data processing capabilities using an in-memory mock data engine. It meets all design and functional specifications without requiring configuration against persistent cloud databases or external system infrastructure.

### 🌟 Core Capabilities Implemented of this project

*   **Lead Velocity Tier:** Top-of-funnel tracking utilizing responsive metric cards detailing aggregate volume, qualification metrics, conversion shifts, and percentage bounces.
*   **Period-over-Period (PoP) Tracking:** Dynamic filtering engines (*Today*, *Last 7 Days*, *Last 30 Days*, and *Custom Ranges*) that instantly compute active metrics and calculate exact delta shifts against equivalent past durations.
*   **Interactive Value Visualization:** Multi-axis charting combinations (Bar, Line, Radial Gauges, and Funnels) built on Plotly to showcase operational trends and target completions.
*   **Granular Drill-Down Layer:** Contextual selector hooks that bridge macroscopic charts down into tabular registry records for clean operational auditing.
*   **Workforce Accountability Logs:** Fully calculated employee leaderboards tracking assigned quotas alongside individual financial conversion metrics.

---

## 🛠️ Technology Stack & Dependencies

*   **Runtime Environment:** Python 3.10+
*   **Application & UI Framework:** Streamlit (Reactive Interface Layer)
*   **Data Processing Core:** Pandas & NumPy (Vectorized Manipulation Engine)
*   **Graphics Engine:** Plotly (Interactive Client-Side Canvas)

---

## 💻 Local Setup & Execution Guide

Follow these steps to run the interactive frontend environment on a Windows environment using VS Code:

### 1. Initialize Project Sandbox
Open your terminal window inside VS Code (`Ctrl + \``) and isolate your environment using `venv`:
```
# Create local virtual environment in vs code
python -m venv venv
# Activate the isolated system environment
.\venv\Scripts\activate
```
*Note: If Windows flags an execution policy script restriction error, resolve it instantly by running `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` before activating.*
### 2. Install Project Requirements
Install the locked interface dependencies using `pip`:
```vs code
pip install -r requirements.txt
```
requirement.txt includes includes streamlit,pandas,plotly,numpy
### 3. Initialize the Application
Boot up the local reactive development server:
```vs code
streamlit run app.py
```
Your default browser will immediately launch a new active viewport tab at `http://localhost:8501`.
---
## 🌐 Cloud Deployment Architecture

This project is deployed live via **Streamlit Community Cloud** infrastructure directly from the source repository. The live production application features fully functional UI responsiveness, date range calculation frameworks, and filter drill-downs.
*   **Deployment Configuration:** Static deployment via GitHub webhooks (`app.py` entry point).
