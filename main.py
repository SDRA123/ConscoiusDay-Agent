from datetime import date, datetime
import streamlit as st
from langchain_openai import ChatOpenAI
from together import Together
import sqlite3
from dotenv import load_dotenv
import os
import re

# Load secrets from .env
load_dotenv(dotenv_path="prod.env")
client = Together(api_key=os.getenv("together_api"))

def create_database():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            journal TEXT,
            intention TEXT,
            dream TEXT,
            priorities TEXT,
            reflection TEXT,
            dream_interpretation TEXT,
            mindset_insight TEXT,
            strategy TEXT
        );
    """)
    conn.commit()
    conn.close()
    print("Database and table created successfully.")

def get_response(journal, intention, dream, priorities):
    prompt = f"""
        You are a daily reflection and planning assistant. Your goal is to:
        1. Reflect on the user's journal and dream input
        2. Interpret the user's emotional and mental state
        3. Understand their intention and 3 priorities
        4. Generate a practical, energy-aligned strategy for their day
        INPUT:
        Morning Journal: {journal}
        Intention: {intention}
        Dream: {dream}
        Top 3 Priorities: {priorities}
        OUTPUT:
        1. Inner Reflection Summary
        2. Dream Interpretation Summary
        3. Energy/Mindset Insight
        4. Suggested Day Strategy (time-aligned tasks)
    """
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating response from AI: {e}")
        return ""

def parse_ai_output(output_string):
    # Improved regex pattern with optional colons, spaces, and bullet formatting
    pattern = re.compile(
        r"(?i)(?:\*\*)?\s*1\.\s*Inner Reflection Summary\s*:?\s*(?:\*\*)?\s*\n(.*?)"
        r"(?:\*\*)?\s*2\.\s*Dream Interpretation Summary\s*:?\s*(?:\*\*)?\s*\n(.*?)"
        r"(?:\*\*)?\s*3\.\s*Energy/Mindset Insight\s*:?\s*(?:\*\*)?\s*\n(.*?)"
        r"(?:\*\*)?\s*4\.\s*Suggested Day Strategy(?:\s*\(.*?\))?\s*:?\s*(?:\*\*)?\s*\n(.*)",
        re.DOTALL
    )

    match = pattern.search(output_string)
    
    if match:
        return {
            "reflection": match.group(1).strip(),
            "dream_interpretation": match.group(2).strip(),
            "mindset_insight": match.group(3).strip(),
            "day_strategy": match.group(4).strip()
        }
    else:
        # Fallback: extract each section independently
        def extract_section(start_label, end_label=None):
            if end_label:
                regex = rf"(?i){start_label}\s*:?\s*\n(.*?)(?=\n{end_label}\s*:?)"
            else:
                regex = rf"(?i){start_label}\s*:?\s*\n(.*)"
            match = re.search(regex, output_string, re.DOTALL)
            return match.group(1).strip() if match else ""

        return {
            "reflection": extract_section("1\\.\\s*Inner Reflection Summary", "2\\.\\s*Dream Interpretation Summary"),
            "dream_interpretation": extract_section("2\\.\\s*Dream Interpretation Summary", "3\\.\\s*Energy/Mindset Insight"),
            "mindset_insight": extract_section("3\\.\\s*Energy/Mindset Insight", "4\\.\\s*Suggested Day Strategy"),
            "day_strategy": extract_section("4\\.\\s*Suggested Day Strategy")
        }
def save_entry(selected_date, journal, intention, dream, priorities, reflection, dream_interpretation, mindset_insight, strategy):
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO entries (date, journal, intention, dream, priorities, reflection, dream_interpretation, mindset_insight, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            journal=excluded.journal,
            intention=excluded.intention,
            dream=excluded.dream,
            priorities=excluded.priorities,
            reflection=excluded.reflection,
            dream_interpretation=excluded.dream_interpretation,
            mindset_insight=excluded.mindset_insight,
            strategy=excluded.strategy
    """, (selected_date, journal, intention, dream, priorities, reflection, dream_interpretation, mindset_insight, strategy))
    conn.commit()
    conn.close()
    st.success(f"Entry for {selected_date} saved successfully!")

def load_entry(selected_date):
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT journal, intention, dream, priorities, reflection, dream_interpretation, mindset_insight, strategy 
        FROM entries WHERE date = ?
    """, (selected_date,))
    entry = cursor.fetchone()
    conn.close()
    return entry

def get_all_dates():
    conn = sqlite3.connect("entries.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date FROM entries ORDER BY date DESC")
    dates = [row[0] for row in cursor.fetchall()]
    conn.close()
    return dates

def main():
    create_database()
    st.set_page_config("Daily Reflection Journal", layout="centered")
    st.title("📝 Daily Reflection Journal")

    today = datetime.now().strftime("%Y-%m-%d")

    # Sidebar to view past entries
    st.sidebar.header("📅 View Previous Entries")
    all_dates = get_all_dates()
    selected_view_date = st.sidebar.selectbox("Select a date", all_dates)

    if selected_view_date and selected_view_date != st.session_state.get("loaded_date"):
        loaded_entry = load_entry(selected_view_date)
        if loaded_entry:
            st.session_state["journal"] = loaded_entry[0]
            st.session_state["intention"] = loaded_entry[1]
            st.session_state["dream"] = loaded_entry[2]
            st.session_state["priorities"] = loaded_entry[3]
            st.session_state["reflection_output"] = loaded_entry[4]
            st.session_state["dream_interpretation_output"] = loaded_entry[5]
            st.session_state["mindset_insight_output"] = loaded_entry[6]
            st.session_state["strategy_output"] = loaded_entry[7]
            st.session_state["loaded_date"] = selected_view_date
            st.sidebar.success(f"Loaded entry for {selected_view_date}")

    # Form Inputs
    st.subheader("✨ Today's Journal")
    journal = st.text_area("Journal Entry", value=st.session_state.get("journal", ""), height=150, key="journal")
    intention = st.text_area("Intention", value=st.session_state.get("intention", ""), height=100, key="intention")
    dream = st.text_area("Dream", value=st.session_state.get("dream", ""), height=100, key="dream")
    priorities = st.text_area("Top 3 Priorities", value=st.session_state.get("priorities", ""), height=100, key="priorities")

    # Generate & Save Insights
    if st.button("✨ Generate Insights"):
        if selected_view_date != today and selected_view_date:
            st.warning("You can only generate or modify insights for today's entry.")
        else:
            with st.spinner("Generating..."):
                output = get_response(journal, intention, dream, priorities)
                parsed_output = parse_ai_output(output)

                st.session_state["reflection_output"] = parsed_output["reflection"]
                st.session_state["dream_interpretation_output"] = parsed_output["dream_interpretation"]
                st.session_state["mindset_insight_output"] = parsed_output["mindset_insight"]
                st.session_state["strategy_output"] = parsed_output["day_strategy"]

                save_entry(
                    selected_date=today,
                    journal=journal,
                    intention=intention,
                    dream=dream,
                    priorities=priorities,
                    reflection=parsed_output["reflection"],
                    dream_interpretation=parsed_output["dream_interpretation"],
                    mindset_insight=parsed_output["mindset_insight"],
                    strategy=parsed_output["day_strategy"]
                )

    # Display Outputs
    if "reflection_output" in st.session_state:
        st.markdown("### 🧘 Reflection")
        st.info(st.session_state["reflection_output"])

    if "dream_interpretation_output" in st.session_state:
        st.markdown("### 🌙 Dream Interpretation")
        st.info(st.session_state["dream_interpretation_output"])

    if "mindset_insight_output" in st.session_state:
        st.markdown("### 🧠 Mindset Insight")
        st.info(st.session_state["mindset_insight_output"])

    if "strategy_output" in st.session_state:
        st.markdown("### 🎯 Strategy")
        st.success(st.session_state["strategy_output"])

if __name__ == "__main__":
    if "loaded_date" not in st.session_state:
        st.session_state["loaded_date"] = ""
    main()
