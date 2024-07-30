from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.set_page_config(page_title="I can Retrieve any SQL query")


def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt, question])
    return response.text


def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        for row in rows:
            print(row)
        return rows
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []


def get_db_schema(db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        schema_info = {}
        for table in tables:
            cur.execute(f"PRAGMA table_info({table[0]});")
            schema_info[table[0]] = cur.fetchall()
        conn.close()
        return schema_info
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving schema: {e}")
        return {}


def generate_prompt(schema_info):
    prompt = "You are an expert in converting English questions to SQL queries!\n"
    prompt += "The SQL database has the following tables and columns:\n"
    
    for table, columns in schema_info.items():
        prompt += f"- Table: {table}\n"
        prompt += "  Columns:\n"
        for col in columns:
            prompt += f"    - {col[1]} ({col[2]})\n"
    
    prompt += "\nFor example,\nExample 1 - How many entries of records are present in a table?, "
    prompt += "the SQL command will be something like this SELECT COUNT(*) FROM <table> ;\n"
    prompt += "Example 2 - Retrieve all records where a specific column has a particular value, "
    prompt += "the SQL command will be something like this SELECT * FROM <table> WHERE <column>='<value>';\n"
    prompt += "Note: Ensure that the SQL code does not have ``` at the beginning or end and does not include the word 'sql'.\n"
    return prompt


st.header("Gemini App to retrieve SQL data")

uploaded_file = st.file_uploader("Upload your SQLite database file", type="db")
question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

if submit and uploaded_file is not None:
    with open("uploaded_student.db", "wb") as f:
        f.write(uploaded_file.getbuffer())

    schema_info = get_db_schema("uploaded_student.db")
    if schema_info:
        prompt = generate_prompt(schema_info)
        response = get_gemini_response(question, prompt)
        print(f"Generated SQL query: {response}")

        data = read_sql_query(response, "uploaded_student.db")
        st.subheader("The response is")
        if data:
            for row in data:
                print(row)
                st.write(row)
        else:
            st.write("No data found or an error occurred.")
    else:
        st.write("Failed to retrieve schema information from the uploaded database.")
