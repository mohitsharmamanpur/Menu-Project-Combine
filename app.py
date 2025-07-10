import streamlit as st

# Import all section functions
from Sections.machine_learning import machine_learning_section
from Sections.Linux import linux_section
from Sections.Windows import windows_section
from Sections.Python import python_automation_section
from Sections.DevOps import devops_section
from Sections.Cloud import cloud_section
from Sections.Agentic_ai import agentic_ai_section
from Sections.Full_stack import full_stack_section
from Sections.Javascript import javascript_tasks_section


st.set_page_config(page_title="Unified Dashboard", layout="centered")
st.sidebar.title("Navigation")

main_choice = st.sidebar.selectbox(
    "Choose Category",
    [
        "Machine Learning", "Linux", "Windows", "Python",
        "DevOps", "Cloud", "Agentic AI", "Full-Stack", "JavaScript"
    ]
)

# Sub-choice selection for relevant domains
sub_choice = None
if main_choice == "DevOps":
    sub_choice = st.sidebar.selectbox("DevOps Tools", ["Jenkins", "Docker", "Kubernetes"])
elif main_choice == "Cloud":
    sub_choice = st.sidebar.selectbox("Cloud Services", ["AWS EC2", "S3 Buckets", "IAM Roles"])
elif main_choice == "Agentic AI":
    sub_choice = st.sidebar.selectbox("AI Projects", ["Chatbot", "Emotion Detector", "Image Classifier"])
elif main_choice == "Full-Stack":
    sub_choice = st.sidebar.selectbox("Stack Components", ["Automation Tasks", "React/Node", "Database"])
elif main_choice == "Python":
    sub_choice = st.sidebar.selectbox(
        "Automating Tasks",
        [
            "Send Whatsap msg", "Send E-mail", "Send Text msg", "Make a Phone call",
            "Post on Linkedin", "Post on Twitter", "Post on Facebook", "Post on Instagram", "Send watsap image"
        ]
    )
elif main_choice == "JavaScript":
    sub_choice = st.sidebar.selectbox(
        "JavaScript Tasks",
        [
            "Take Photo",
            "Send Email via JS",
            "Send Captured Photo via Email",
            "Record Video and Send via Email",
            "Send WhatsApp Message",
            "Send SMS via JS",
            "Show Current Location",
            "Google Maps Live View",
            "Route from My Location to Destination",
            "Nearby Grocery Stores",
            "Fetch Last Gmail Email Info",
            "Post to Social Media",
            "Track Most Viewed Products",
            "Get IP and Location"
        ]
    )

if main_choice == "Machine Learning":
    machine_learning_section()
elif main_choice == "Linux":
    linux_section()
elif main_choice == "Windows":
    windows_section()
elif main_choice == "Python":
    python_automation_section(sub_choice)
elif main_choice == "DevOps":
    devops_section(sub_choice)
elif main_choice == "Cloud":
    cloud_section(sub_choice)
elif main_choice == "Agentic AI":
    agentic_ai_section(sub_choice)
elif main_choice == "Full-Stack":
    full_stack_section()
elif main_choice == "JavaScript":
    javascript_tasks_section(sub_choice)
else:
    st.write("Please select a category from the sidebar.")
