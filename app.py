import streamlit as st
from datetime import date
from agents import run_eod_agent

# Set the page layout for better display
st.set_page_config(page_title="EOD Report Generator", layout="wide")

# Streamlit UI setup
st.title("📧 End of Day (EOD) Report Generator")
st.markdown("""
    Welcome to the **EOD Report Generator**. This tool helps you create a structured and professional **End of Day** report with ease.
    Simply fill in the details of your day, and we will handle the rest!  
    _(Fields marked with an asterisk (*) are required)_
""")

# Input section
st.sidebar.header("📝 Input your EOD details")
report_date = st.sidebar.date_input("Select Date for the EOD Report", value=date.today(), help="Choose the date of the report")

# Task Input Section
tasks_completed = st.text_area("Tasks Completed *", placeholder="e.g., Ran RA execution, reconciled reports, etc.", height=150)
miscellaneous = st.text_area("Miscellaneous (Optional)", placeholder="e.g., Delayed approvals, system bugs, etc.", height=100)

# Generate EOD Report Button
if st.button("Generate EOD Report"):
    if not tasks_completed.strip():
        st.error("Tasks Completed is a required field.")
    else:
        with st.spinner("Generating your EOD Report..."):
            result = run_eod_agent(tasks_completed, miscellaneous, report_date)
            
            # Display the result
            st.success("Your EOD Report has been generated!")
            st.markdown("### 📧 Final EOD Report")
            
            # Format the result for easy copy-paste in a nice text area
            st.text_area("Generated EOD Report:", result, height=300, disabled=False)

# Add styling for a clean and modern interface
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        padding: 30px;
    }
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #e9ecef;
        border: 1px solid #ced4da;
        padding: 15px;
    }
    .stButton button {
        background-color: #17a2b8;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #138496;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)
