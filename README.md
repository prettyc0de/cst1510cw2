# Streamlit - Multi-Domain Intelligence Platform

## Project Overview
This project is a unified Python and Streamlit web application developed for the **CST1510 Programming for Data Communication and Networks** coursework. It is designed to provide analysis, insights, and operational support for different technical domains.

The platform was originally planned around three user groups:
- **Cybersecurity Analysts**
- **Data Scientists**
- **IT Administrators**

For this submission, the main implemented domains are:
- **Cybersecurity**
- **Data Science**

This project is presented as a **Tier 2 implementation attempt** because it includes two domain dashboards within the same platform.

## Problems Addressed
This project focuses on the following domain problems:

- **Cybersecurity:** analysing phishing incident trends and identifying possible response bottlenecks caused by unresolved or open incidents.
- **Data Science:** analysing dataset metadata, storage size, ownership, and upload activity to support governance and archiving decisions.

The database structure also includes support for:
- **IT Operations:** service desk performance and ticket resolution delays

## Key Technical Features
- **Secure Authentication:** user registration and login with password hashing using `bcrypt`
- **Database Management:** SQLite database for persistent storage of users and domain data
- **Interactive Dashboards:** Streamlit multi-page interface for Cybersecurity and Data Science analysis
- **Data Visualisation:** charts created using Plotly and pandas
- **AI Assistant:** beginner-friendly cybersecurity chatbot using an external LLM API
- **Modular Code Structure:** project separated into multiple Python files for better organisation and maintainability

## Implemented Tier
This coursework submission is a **Tier 2 implementation attempt**.

### Implemented Domains
- **Cybersecurity Dashboard**
- **Data Science Dashboard**

## Project Structure
Main files used in this project include:

- `Home.py`
- `pages/1_Cyber_Security.py`
- `pages/2_Data_Science.py`
- `pages/chat_GPT.py`
- `app_model/db.py`
- `app_model/users.py`
- `app_model/cyber_incidents.py`
- `app_model/metadatas.py`
- `requirements.txt`

## Technologies Used
- **Python**
- **Streamlit**
- **SQLite**
- **pandas**
- **Plotly**
- **bcrypt**
- **Groq API**

## Getting Started

### 1. Install dependencies
    pip install -r requirements.txt

### 2. Set up the API key
Set your Groq API key in the terminal before running the project:

    set GROQ_API_KEY=your_api_key_here

### 3. Run the application
    streamlit run Home.py

## Main Features by Domain

### Cybersecurity Dashboard
The Cybersecurity dashboard was developed to support the analysis of incident data. It helps identify possible phishing trends and unresolved incident bottlenecks through:
- incident count metrics
- phishing-related insights
- severity distribution charts
- trend analysis over time
- filtered incident table

### Data Science Dashboard
The Data Science dashboard was developed to support dataset governance and storage planning. It helps identify:
- large datasets
- upload ownership patterns
- upload trends over time
- row and column comparisons
- possible archiving or validation priorities

### AI Assistant
The AI assistant provides simple cybersecurity support for users. It can answer short questions related to:
- phishing
- cyber incidents
- dashboard understanding
- response actions

## Notes
- The application uses **bcrypt** to securely hash passwords.
- The application uses **SQLite** for local persistent data storage.
- The AI assistant requires a valid **Groq API key** to work.
- The project was developed in a beginner-friendly modular style rather than as a highly advanced enterprise system.

## GitHub Repository
- **https://github.com/prettyc0de/cst1510cw2.git**

## Author
**Name:** Faria Fairuz Khan Pritika  
**Student ID:** M01101914  
**Program:** AI and Data Science (2025–26)  
**Module:** CST1510 Programming for Data Communication and Networks