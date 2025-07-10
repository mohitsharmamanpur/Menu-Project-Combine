import streamlit as st

def cloud_section(sub_choice=None):
    st.header("☁️ Cloud Services")
    st.info(f"Selected: {sub_choice}")
    st.write("This is a placeholder for Cloud services integration.")
    st.write("You can add AWS EC2, S3, or IAM controls here.")
