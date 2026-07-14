# Global Malaria Incidence and Deaths Analysis 

**Deus Tumusiime** (Reg. No: **2025/HD05/26375U**).
- `MCS 7227`: DATA ANALYTICS & VISUALIZATION                                                                                                                                               
- `By`: JJINGO DAUDI PHD, & HENRY MUTEGEKI
- MAKERERE UNIVERSITY

## Project Overview
This project provides an end-to-end data analytics and visualization pipeline for the WHO estimated malaria numbers dataset (covering 107 countries over 2010–2017). It includes:
1. **Part A & B**: Rigorous data exploration, data quality audit (missing bounds analysis, consistency checks, character encoding standardization), and structural preprocessing.
2. **Part C**: Comprehensive data visualizations (univariate, bivariate, multivariate, temporal, and an interactive geographic map) with statistical interpretations, alongside Pearson/Spearman correlation and three inferential hypothesis tests.
3. **Part D**: Environment documentation, reproducibility guidelines, and a formal Word report containing figure embeddings and citations.
4. **Bonus Task**: An interactive Streamlit dashboard allowing users to filter and inspect malaria transmission metrics dynamically.

---

## Deliverables in this Archive

- `malaria_analysis.ipynb`: The primary Jupyter Notebook containing all markdown documentation, python code, and inline output cells (visuals and statistical results).
- `DEUS_TUMUSIIME_2025_HD05_26375U.docx`: A formal, structured academic Word report with embedded high-resolution figures, in-depth methodology write-up, and key findings.
- `app.py`: The python script containing the interactive Streamlit dashboard.
- `estimated_numbers-selected-columns.csv`: The original, raw Kaggle/WHO dataset used for analysis.
- `estimated_numbers_cleaned.csv`: The cleaned, imputed, and externally enriched dataset.
- `estimated_numbers_cleaned_encoded.csv`: The final preprocessed dataset including one-hot encoded WHO regions and ordinal-encoded burden categories.
- `figures/`: A folder containing all 13 high-resolution PNG charts generated from the notebook and the dashboard screenshot, embedded in the report.
- `README.md`: This configuration and guide document.

---

## Tested Environment

### Local Tested Environment
- **Python**: 3.13.5
- **Streamlit**: 1.45.1
- **Operating System**: Windows

### Deployed Environment (Streamlit Community Cloud)
- **Deployment URL**: https://global-malaria-trends-4vhcxue7bwn4dhgt9tr4k3.streamlit.app
- **Hosting Platform**: Streamlit Community Cloud (connected to the GitHub repository main branch)

### Repo on Github (Public Repository)
- **Repository URL**: https://github.com/deusrapha/global-malaria-trends

---

## Environment Setup and Installation

To reproduce the analysis and run the interactive dashboard, ensure you have Python 3.8+ installed. You can install all necessary packages by running:

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels plotly streamlit python-docx
```

### 1. Running the Jupyter Notebook
You can open and execute the notebook in any Jupyter environment (e.g. JupyterLab, VS Code, Google Colab):
```bash
jupyter notebook malaria_analysis.ipynb
```
Select **Kernel > Restart & Run All** to verify that it executes from top to bottom with zero errors.

### 2. Running the Interactive Dashboard
To launch the Streamlit dashboard locally, run the following command in the project directory:
```bash
streamlit run app.py
```
This will start a local web server (usually at `http://localhost:8501`) and open the dashboard in your default browser.

### 3. Reviewing the Report
Open the `DEUS_TUMUSIIME_2025_HD05_26375U.docx` file in Microsoft Word or any compatible document editor to review the formal academic report.
