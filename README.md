
````markdown
# ConsiousDay Agent

A simple journaling web app agent built with [Streamlit](https://streamlit.io) that uses AI (LLaMA-3-70B via [Together API](https://www.together.ai/)) to help you reflect and plan your day. The app stores entries in a local SQLite database and generates insights based on your journal input, intention, dream, and daily priorities.

---

## Features

- Input your:
  - Daily journal entry
  - Intention for the day
  - Dream (if any)
  - Top 3 priorities
- AI-generated insights including:
  - Inner reflection
  - Dream interpretation
  - Mindset insight
  - Suggested day strategy
- Save and update daily entries
- View past entries from a calendar dropdown

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/daily-reflection-journal.git
cd daily-reflection-journal
````

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your API Key

Create a `.env` file in the root folder and add your [Together API](https://www.together.ai/) key:

```env
together_api=your_together_api_key_here
```

If deploying on **Streamlit Cloud**, use **Secrets Manager** instead of `.env`.

### 4. Run the Application

```bash
streamlit run app.py
```

---

## Project Structure

```
.
├── app.py                # Main Streamlit application
├── entries.db            # SQLite database (created on first run)
├── .env                  # API key file (for local use only)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Technologies Used

* Python
* Streamlit
* Together API (LLaMA-3-70B)
* SQLite
* Regular Expressions (for parsing AI output)

---

## Notes

* Requires a Together API key (get one at [https://www.together.ai/](https://www.together.ai/))
* Entries are stored locally in `entries.db`
* Only today's entry can be generated or edited
* Previous entries are read-only

---




