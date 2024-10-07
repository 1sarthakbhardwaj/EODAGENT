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
    _(Fields marked with an asterisk (*) are required)_.
""")

# Dark mode toggle button
dark_mode = st.sidebar.checkbox("🌗 Toggle Dark Mode")

# Apply light/dark mode CSS dynamically
if dark_mode:
    page_bg_color = "#2e2e2e"
    text_color = "#ffffff"
    text_area_bg = "#424242"
    button_bg = "#17a2b8"
    button_hover_bg = "#138496"
else:
    page_bg_color = "#f8f9fa"
    text_color = "#000000"
    text_area_bg = "#ffffff"
    button_bg = "#17a2b8"
    button_hover_bg = "#138496"

# Custom CSS to toggle light/dark mode and apply other styles
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {page_bg_color};
        color: {text_color};
        padding: 30px;
    }}
    .stTextArea textarea {{
        background-color: {text_area_bg};
        color: {text_color};
        border: 1px solid #ced4da;
        padding: 15px;
    }}
    .stButton button {{
        background-color: {button_bg};
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }}
    .stButton button:hover {{
        background-color: {button_hover_bg};
        color: white;
    }}
    </style>
""", unsafe_allow_html=True)

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

            # Add a copy button (Streamlit doesn't support native clipboard access, so using JavaScript)
            st.markdown(f"""
                <button onclick="navigator.clipboard.writeText(`{result}`)" 
                    style="background-color:{button_bg}; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer">
                    Copy Report to Clipboard
                </button>
            """, unsafe_allow_html=True)
