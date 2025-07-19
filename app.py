import streamlit as st
import os
from datetime import datetime

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

# Page configuration
# st.set_page_config(
#     page_title="Universal Automation Platform",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Custom CSS for better styling and background image
st.markdown("""
<style>
body, .stApp {
    background-image: linear-gradient(rgba(30,30,30,0.85), rgba(30,30,30,0.85)), url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    color: #1f77b4;
    margin-bottom: 2rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.section-header {
    font-size: 2rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 1rem;
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.5rem;
}
.feature-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    margin: 1rem 0;
}
.metric-card {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #007bff;
    margin: 0.5rem 0;
}
.success-box {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
.warning-box {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# --- Password Protection ---
PASSWORD = "admin123"  # Set your password here

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Enter Password to Access the App")
    password_input = st.text_input("Password", type="password")
    if st.button("Login"):
        if password_input == PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted!")
            st.rerun()
        else:
            st.error("Incorrect password. Try again.")
    st.stop()  # Prevents the rest of the app from running if not authenticated

# Initialize session state for dark_mode
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Sidebar configuration
with st.sidebar:
    st.title("🚀 Universal Automation Platform")
    
    # Dark mode toggle
    dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    st.divider()
    
    # Main navigation
    st.subheader("📚 Main Categories")
    main_choice = st.selectbox(
        "Choose Category",
        [
            "🏠 Dashboard",
            "🧠 Machine Learning", 
            "🐧 Linux", 
            "🪟 Windows", 
            "🐍 Python",
            "⚙️ DevOps", 
            "☁️ Cloud", 
            "🤖 Agentic AI", 
            "🌐 Full-Stack", 
            "📱 JavaScript"
        ],
        index=0
    )
    
    # Sub-choice selection for relevant domains
    sub_choice = None
    if main_choice == "⚙️ DevOps":
        sub_choice = st.selectbox("DevOps Tools", ["🐳 Docker", "⚙️ Jenkins", "☸️ Kubernetes"])
    elif main_choice == "☁️ Cloud":
        sub_choice = st.selectbox("Cloud Services", ["🚀 AWS EC2", "📦 S3 Buckets", "🔐 IAM Roles", "💾 EBS Volumes"])
    elif main_choice == "🤖 Agentic AI":
        sub_choice = st.selectbox("AI Projects", ["💬 Chatbot", "📄 Document Q&A", "📝 AI Summarizer", "🎯 Task Executor"])
    elif main_choice == "🌐 Full-Stack":
        sub_choice = st.selectbox("Stack Components", ["🤖 Automation Tasks", "⚛️ React/Node", "🗄️ Database"])
    elif main_choice == "🐍 Python":
        sub_choice = st.selectbox(
            "Automating Tasks",
            [
                "📱 Send WhatsApp msg", "📧 Send E-mail", "📲 Send Text msg", "📞 Make a Phone call",
                "💼 Post on LinkedIn", "🐦 Post on Twitter", "📘 Post on Facebook", "📷 Post on Instagram", 
                "🖼️ Send WhatsApp image", "🌐 Web Scraping", "📸 Screenshot", "💻 System Monitor"
            ]
        )
    elif main_choice == "📱 JavaScript":
        sub_choice = st.selectbox(
            "JavaScript Tasks",
            [
                "📸 Take Photo", "📧 Send Email via JS", "📷 Send Captured Photo via Email",
                "🎥 Record Video and Send via Email", "📱 Send WhatsApp Message", "📲 Send SMS via JS",
                "📍 Show Current Location", "🗺️ Google Maps Live View", "🛣️ Route Navigation",
                "🏪 Nearby Grocery Stores", "📧 Fetch Last Gmail Email Info", "📱 Post to Social Media",
                "📊 Track Most Viewed Products", "🌍 Get IP and Location"
            ]
        )
    
    st.divider()
    # (Removed old login/logout logic here)

# Main content area
if main_choice == "🏠 Dashboard":
    st.markdown('<h1 class="main-header">🚀 Universal Automation Platform</h1>', unsafe_allow_html=True)
    
    # Dashboard overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Total Tasks", "50+", "9 Categories")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🤖 AI Models", "5+", "ML & AI Tasks")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("☁️ Cloud Services", "4+", "AWS Integration")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("⚙️ DevOps Tools", "3+", "Docker, Jenkins, K8s")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Feature highlights
    st.markdown('<h2 class="section-header">🌟 Platform Features</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🧠 Machine Learning")
        st.write("• Upload and analyze datasets")
        st.write("• Train ML models (SVM, Random Forest)")
        st.write("• Visualize results with charts")
        st.write("• Make predictions from user input")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("⚙️ DevOps Automation")
        st.write("• Docker container management")
        st.write("• Jenkins job automation")
        st.write("• Kubernetes deployment")
        st.write("• CI/CD pipeline control")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🤖 Agentic AI")
        st.write("• OpenAI/Gemini integration")
        st.write("• Chat with AI agents")
        st.write("• Document Q&A system")
        st.write("• Context-aware conversations")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("☁️ Cloud Services")
        st.write("• AWS EC2 instance management")
        st.write("• S3 file operations")
        st.write("• EBS volume management")
        st.write("• Security group configuration")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("🌐 Full-Stack Development")
        st.write("• React/Node.js integration")
        st.write("• Database operations")
        st.write("• API development")
        st.write("• Web automation tasks")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.subheader("📱 JavaScript Tasks")
        st.write("• Camera and media capture")
        st.write("• Location services")
        st.write("• Social media integration")
        st.write("• Browser automation")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent activity
    st.divider()
    st.markdown('<h2 class="section-header">📈 Recent Activity</h2>', unsafe_allow_html=True)
    
    # Check if command log exists
    if os.path.exists("command_log.txt"):
        with open("command_log.txt", "r") as f:
            recent_commands = f.readlines()[-10:]  # Last 10 commands
        
        if recent_commands:
            for cmd in recent_commands:
                st.text(f"🕒 {cmd.strip()}")
        else:
            st.info("No recent activity. Start using the platform to see your actions here!")
    else:
        st.info("No activity log found. Your actions will be logged here!")

elif main_choice == "🧠 Machine Learning":
    machine_learning_section()
elif main_choice == "🐧 Linux":
    linux_section()
elif main_choice == "🪟 Windows":
    windows_section()
elif main_choice == "🐍 Python":
    python_automation_section(sub_choice)
elif main_choice == "⚙️ DevOps":
    devops_section(sub_choice)
elif main_choice == "☁️ Cloud":
    cloud_section(sub_choice)
elif main_choice == "🤖 Agentic AI":
    agentic_ai_section(sub_choice)
elif main_choice == "🌐 Full-Stack":
    full_stack_section(sub_choice)
elif main_choice == "📱 JavaScript":
    javascript_tasks_section(sub_choice)
else:
    st.write("Please select a category from the sidebar.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🚀 Universal Automation Platform | Built with Streamlit | Version 2.0</p>
    <p>© 2024 - All rights reserved</p>
</div>
""", unsafe_allow_html=True)
