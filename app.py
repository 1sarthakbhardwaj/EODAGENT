import streamlit as st
from agents import run_eod_agent

# Set the page layout for better display
st.set_page_config(page_title="EOD Report Generator", layout="wide")

# Custom CSS for improving the style
st.markdown("""
    <style>
    body, .stApp {
        background-color: #f4f4f9;  /* Light background for contrast */
    }
    .report-box {
        background-color: #ffffff;  /* White background for the generated report */
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        font-family: 'Segoe UI', sans-serif;
        font-size: 1.1rem;
        color: #333;  /* Darker text for readability */
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI setup
st.title("📧 End of Day (EOD) Report Generator")
st.markdown("""
    This tool helps you generate a well-structured **EOD report** for submission.  
    Fill out your daily details, and let the system draft a professional email.
""")

# Date input
date = st.date_input("Select Date for the EOD Report")

# Input fields for tasks and miscellaneous
tasks_completed = st.text_area("Tasks Completed *", placeholder="Ran RA execution, reconciled reports, etc.", height=150)
miscellaneous = st.text_area("Miscellaneous (Optional)", placeholder="Any delayed approvals, system bugs, etc.", height=100)

# Button to generate EOD report
if st.button("Generate EOD Report"):
    if not tasks_completed.strip():
        st.error("Tasks Completed is a required field.")
    else:
        with st.spinner("Generating your EOD Report..."):
            result = run_eod_agent(tasks_completed, miscellaneous)
            
            # Display the result in a styled box
            st.success("EOD Report Generated!")
            st.markdown("### 📧 Final EOD Report")
            
            st.markdown(f"""
                <div class='report-box'>
                    <p><b>Subject: EOD Report - {date}</b></p>
                    <p>Dear Prashar Katyal,</p>
                    <p><b>Tasks Completed:</b></p>
                    <p>{result['tasks_completed']}</p>
                    {f"<p><b>Miscellaneous:</b></p><p>{result['miscellaneous']}</p>" if result['miscellaneous'] else ''}
                    <p>Best regards,<br>Sarthak Bhardwaj<br>Associate Software Engineer, Amdocs</p>
                </div>
            """, unsafe_allow_html=True)

# Add padding for the app
st.markdown("""
    <style>
    .stApp {
        padding: 30px;
    }
    </style>
""", unsafe_allow_html=True)
