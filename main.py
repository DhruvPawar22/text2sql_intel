from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

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
        return rows
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

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
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")

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

@app.post("/upload/")
async def upload_db(file: UploadFile = File(...)):
    file_location = f"uploaded_student.db"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": "File uploaded successfully"}

@app.post("/query/")
async def query_database(request: QueryRequest):
    schema_info = get_db_schema("uploaded_student.db")
    if schema_info:
        prompt = generate_prompt(schema_info)
        response = get_gemini_response(request.question, prompt)
        data = read_sql_query(response, "uploaded_student.db")
        return {"data": data}
    else:
        raise HTTPException(status_code=500, detail="Failed to retrieve schema information")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
