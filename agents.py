import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize the Groq LLM
llm = ChatGroq(
    temperature=0,
    model_name="llama3-70b-8192",
    api_key=api_key
)

# Define agents
mail_drafter = Agent(
    llm=llm,
    role="Mail Generator for EOD Report",
    goal=("Generate a well-structured and concise End Of Day report mail addressed to your Team Lead: "
          "Prashar Katyal. Detailing tasks completed: {tasks_completed} and any miscellaneous notes: {miscellaneous}, "
          "for the date: {report_date}."),
    backstory="You're Sarthak Bhardwaj, an Associate Software Engineer working with Amdocs. You write a daily EOD mail to Prashar Katyal.",
    allow_delegation=False,
    verbose=True
)

mail_validator = Agent(
    llm=llm,
    role="Validate the EOD Report",
    goal="Ensure the report generated by the Mail Drafter is accurate and coherent. Validate content for context.",
    backstory="You ensure that the EOD mail is clear and in professional tone.",
    allow_delegation=False,
    verbose=True
)

# Define tasks
report_task = Task(
    description="Generate an EOD report covering tasks completed and any miscellaneous details for {report_date}.",
    expected_output="A structured EOD report with sections for tasks completed and miscellaneous details.",
    agent=mail_drafter
)

validator_task = Task(
    description="Validate the EOD mail for context and clarity.",
    expected_output="Ensure the mail is in the right context and has no irrelevant information.",
    agent=mail_validator,
    context=[report_task]
)

# Create the Crew
crew = Crew(
    agents=[mail_drafter, mail_validator],
    tasks=[report_task, validator_task],
    verbose=True
)

# Function to run the EOD agent
def run_eod_agent(tasks_completed, miscellaneous, report_date):
    # Input dictionary for the EOD report
    inputs = {
        "tasks_completed": tasks_completed,
        "miscellaneous": miscellaneous.strip() if miscellaneous.strip() else None,  # Exclude if empty
        "report_date": report_date
    }

    # Execute the crew with dynamic inputs
    final_output = crew.kickoff(inputs=inputs)

    # Return the final output
    return final_output

# Example execution (if running locally)
if __name__ == "__main__":
    tasks_completed = "- Completed BAU tasks\n- Ran reconciliations\n- Sent execution mails"
    miscellaneous = ""  # No miscellaneous tasks for today
    report_date = "2024-10-01"

    result = run_eod_agent(tasks_completed, miscellaneous, report_date)
    print("EOD Report:")
    print(result)
