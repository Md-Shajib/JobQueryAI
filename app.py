import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
import ollama
from flask_cors import CORS
import torch

# Get absolute paths for templates and static folders
template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Initialize Flask app
app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
CORS(app)

# Load CSV data
df = pd.read_csv("jobs_data.csv")

# Function to filter jobs based on criteria
def filter_jobs(query, job_data):
    filters = {
        "experience": ["1-2 years", "2-5 years", "5+ years"],
        "skills": "skills",
        "location": "location",
        "salary": "salary",
        "intern": "intern" 
    }
    for key, value in filters.items():
        if key in query.lower():
            if isinstance(value, list):
                match = next((exp for exp in value if exp.lower() in query.lower()), None)
                if match:
                    job_data = job_data[job_data["Job Description"].str.contains(match, case=False, na=False)]
            else:
                param = query.split(value)[-1].strip()
                col = "Job Title" if key == "intern" else "Location" if key == "location" else "Salary" if key == "salary" else "Job Description"
                job_data = job_data[job_data[col].str.contains(param, case=False, na=False)]
    return job_data

# Function to generate LLM response
def get_answer(query, job_data):
    context = "\n".join(job_data["Job Title"].head(5).tolist())  # Use only top 5 job titles
    model_response = ollama.chat(model="llama3.2:latest", messages=[
        {"role": "system", "content": "Provide a short and precise answer within 50 words."},
        {"role": "user", "content": f"{query}\n\n{context}"}
    ])
    return model_response["message"]["content"]

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# API route for answering questions
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400
    # Filter jobs based on query
    filtered_data = filter_jobs(question, df)
    # If no job data matches the query, return a default response
    if filtered_data.empty:
        return jsonify({"answer": "No matching jobs found."})
    # Get AI-generated answer with concise output
    answer = get_answer(question, filtered_data)
    return jsonify({"answer": answer})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
