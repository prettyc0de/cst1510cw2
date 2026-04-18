# Streamlit - Multi-Domain Intelligence Platform 

## Project Overview
A unified Python and Streamlit web application designed to provide data analysis, insights, and operational capabilities for three distinct user groups: Cybersecurity Analysts, Data Scientists, and IT Administrators. 

## Addressed Problems 
Visualisatio Data Set related to the following data set: 
- **Cybersecurity:** Analyzing spikes in phishing incidents and incident response bottlenecks.
- **Data Science:** Managing large datasets, analyzing resource consumption, and recommending data governance policies.
- **IT Operations:** Identifying process inefficiencies and staff performance anomalies causing delays in ticket resolution.

## Key Technical Features
- **Secure Authentication:** Password hashing and verification using `bcrypt`.
- **Database Management:** SQL-based CRUD operations using SQLite for persistent multi-domain data storage.
- **Interactive Dashboards:** Streamlit multi-page web interface with dynamic data visualizations using Plotly/Matplotlib.
- **AI Integration:** Context-aware AI assistant powered by the OpenAI API to support analysts.
- **Object-Oriented Design:** Maintainable codebase refactored using OOP principles and the MVC architecture (optional)

## Getting Started

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment variables:**
   - Add your `OPENAI_API_KEY` for the AI integration to work.

3. **Run the application:**
   ```bash
   streamlit run Home.py
   ```

## Author
Student Name – CST01510 – 2025/26