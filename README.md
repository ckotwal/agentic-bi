# Data Visualization Agent with Generative AI
This project demonstrates how to build a data visualization agent using OpenAI's GPT-4, LangChain, and Streamlit. The agent interacts with a BigQuery database to perform data analysis and generate charts and maps based on natural language queries.

## Features
- Natural Language Interface: Ask questions about your data using natural language.
- Automated SQL Generation: Converts natural language queries into SQL queries.
- Dynamic Data Visualization: Recommends and generates appropriate visualizations (bar charts, line chart, pie charts, scatter plots, maps).
- Real-Time Feedback: Provides real-time status updates in the Streamlit interface using custom event handlers.
- Geographical Data Handling: Extracts coordinates from data for map visualizations.

## Prerequisites
- Python 3.7 or later
- Google Cloud Account: Access to a BigQuery database.
- OpenAI API Key

## Installation
```
pip install streamlit langchain openai google-cloud-bigquery pandas "langchain-google-community[bigquery]" python-dotenv langchain_openai plotly
```

## Setting Up the Database

```
CREATE TABLE `your_project.your_dataset.customer` (
    customer_key STRING NOT NULL,
    first_name STRING,
    last_name STRING,
    source_system_name STRING,
    dob DATE,
    gender STRING,
    create_timestamp TIMESTAMP
);

CREATE TABLE `your_project.your_dataset.customer_address` (
    customer_key STRING NOT NULL,
    address_key STRING NOT NULL
);

CREATE TABLE `your_project.your_dataset.address` (
    address_key STRING NOT NULL,
    full_address STRING,
    state STRING,
    country STRING,
    latitude STRING,
    longitude STRING
);
```

## Running the Application
Start the Streamlit app by running:

```
streamlit run main.py
```

## Example Queries
- "How many customers do we have in each state?"
- "Show me the customer registration trends over the last year."
- "What is the gender distribution of our customers?"
- "Where are our customers located?"