# AI-Powered Data Visualization Assistant

An intelligent data exploration tool that transforms natural language queries into interactive visualizations and insights. Built with Python, Streamlit, and modern AI technologies, this application helps users explore and understand their data through conversational interactions.

## ✨ Features

- **Natural Language to Visualization**: Transform plain English questions into insightful visualizations
- **Interactive Chat Interface**: Built with Streamlit for a seamless user experience
- **Multiple Visualization Types**: Supports various chart types including bar, line, pie, and scatter plots
- **SQL Query Generation**: Automatically generates and executes SQL queries based on user questions
- **Entity Relationship (ER) Diagram Generation**: Visualize database schema and relationships
- **Responsive Design**: Works with different screen sizes and devices
- **Extensible Architecture**: Modular design for easy addition of new visualization types and data sources

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or later
- SQLite database (Chinook sample database included)
- OpenAI API key for AI capabilities
- Required Python packages (see Installation)

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI-DATA-VISUALIZATION-ASSISTANT
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the root directory with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## 🗃️ Database Setup

The project uses SQLite with the Chinook sample database by default. The database file `chinook.db` is already included in the repository.

### Database Schema

The Chinook database includes tables like:
- `artists`
- `albums`
- `tracks`
- `customers`
- `invoices`
- `invoice_items`
- `playlists`
- `playlist_track`
- `employees`
- `genres`
- `media_types`

## 🚀 Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run src/chatbot_ui.py
   ```

2. Open your browser and navigate to `http://localhost:8501`

3. Start asking questions about your data in natural language, such as:
   - "Show me total sales by country"
   - "What are the top 10 selling artists?"
   - "Display a pie chart of genre distribution"
   - "Generate an ER diagram of the database"

## 📊 Example Queries

- "Show total sales by country"
- "What are the top 10 selling artists?"
- "Display a pie chart of genre distribution"
- "Show me the relationship between track length and popularity"
- "Generate an ER diagram of the database"
- "What's the average invoice total by country?"
- "Show me monthly sales trends over time"

## 🏗️ Project Structure

```
AI-DATA-VISUALIZATION-ASSISTANT/
├── .streamlit/           # Streamlit configuration
├── images/               # Static images and assets
├── src/                  # Source code
│   ├── core/             # Core functionality
│   │   ├── viz_tools.py  # Visualization utilities
│   │   └── gen_bi_react_agent.py  # AI agent implementation
│   ├── utils/            # Utility functions
│   └── chatbot_ui.py     # Main Streamlit application
├── tests/                # Test files
├── .env                  # Environment variables
├── chinook.db            # Sample SQLite database
├── main.py               # Legacy entry point
├── README.md             # This file
└── requirements.txt      # Project dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
