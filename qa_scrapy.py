import pandas as pd
import ollama

# Function to filter jobs by experience before querying AI
def filter_jobs_by_experience(job_data, experience_range):
    """Filters jobs based on experience keywords in the description"""
    filtered_jobs = job_data[job_data["Job Description"].str.contains(experience_range, case=False, na=False)]
    return filtered_jobs

# Function to filter jobs by skill before querying AI
def filter_jobs_by_skill(job_data, skill):
    """Filters jobs based on skill keywords in the description"""
    filtered_jobs = job_data[job_data["Job Description"].str.contains(skill, case=False, na=False)]
    return filtered_jobs

# Function to query AI model
def query_jobs(query):
    print("Querying model...")

    # Modify query to force short responses
    query = f"Answer in 3-4 sentences. {query}"

    try:
        # Use llama3.2:3b model
        response = ollama.chat(
            model="llama3.2:latest",  # Use llama3.2:3b model
            messages=[
                {"role": "system", "content": "Provide only relevant job information in short format. Do NOT explain. Keep responses under 100 words."},
                {"role": "user", "content": query}
            ]
        )
        print("Response received.")
        return response["message"]["content"]
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, there was an error processing the query."

# Main function
def main():
    print("Starting script...")

    # Load job data from CSV
    try:
        job_data = pd.read_csv("jobs.csv")
        print(f"Loaded {len(job_data)} job entries.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # Start the loop for continuous queries
    while True:
        query = input("\nWhat would you like to know? Example: 'Give me all intern job summary?' (Type 'exit' to quit) ")
        
        # Allow the user to exit
        if query.lower() == 'exit':
            print("Exiting the program...")
            break

        print(f"\nProcessing query: {query}")

        # Handle experience-based queries with filtering
        if "experience" in query.lower():
            experience_range = "1-2 years"
            filtered_data = filter_jobs_by_experience(job_data, experience_range)
            if not filtered_data.empty:
                print("\n📢 Query Result (Filtered from CSV):\n")
                print(filtered_data.to_string(index=False))
                continue  # Allow user to ask for more questions

        # Handle skill-based queries with filtering
        if "skills" in query.lower():
            skill = query.split("skills")[-1].strip()
            filtered_data = filter_jobs_by_skill(job_data, skill)
            if not filtered_data.empty():
                print("\n📢 Query Result (Filtered from CSV):\n")
                print(filtered_data.to_string(index=False))
                continue  # Allow user to ask for more questions

        # If no direct filter applies, query AI model
        result = query_jobs(query)
        print("\n📢 Query Result:\n", result)

# Corrected main execution entry
if __name__ == "__main__":
    main()
