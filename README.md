Daily Reflection Journal
This is a web-based journaling application built with Streamlit. It helps you reflect on your day and plan ahead by using an AI model to generate insights based on your journal entry, intention, dream, and top 3 priorities.

The app uses the Together.ai API (LLaMA-3-70B) to generate summaries and strategies, and stores all data in a local SQLite database so you can revisit your entries anytime.

Features
Write your daily journal, intention, dream, and top 3 priorities

Get AI-generated insights including:

Inner reflection

Dream interpretation

Mindset insight

Suggested day strategy

Save entries for each date and update them

View and load past entries from a dropdown menu

How to Run
1. Clone the repository
git clone https://github.com/yourusername/daily-reflection-journal.git
cd daily-reflection-journal

3. Install dependencies
pip install -r requirements.txt

4. Set up your API key
Create a .env file in the project root and add your Together API key:

together_api=your_together_api_key_here
If you're deploying on Streamlit Cloud, use the Secrets Manager instead of a .env file.

4. Start the application
streamlit run app.py


Project Structure

.
├── app.py                # Main Streamlit application
├── entries.db            # SQLite database (created on first run)
├── .env                  # API key file (optional for local use)
├── requirements.txt      # List of dependencies
└── README.md             # Project documentation
Technologies Used
Python

Streamlit

Together API (LLaMA-3-70B)

SQLite

Regular Expressions (for parsing AI output)

Notes
You must have an API key from Together.ai

All data is stored locally in a SQLite database file

You can only generate or edit entries for today’s date

Previous entries are read-only

Future Improvements
Use a cloud database to support multiple users

Add login functionality

Mobile-friendly layout

Notification or email reminders

Option to export entries to PDF or Google Docs

