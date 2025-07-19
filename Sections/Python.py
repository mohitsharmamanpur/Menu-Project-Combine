import streamlit as st
import pywhatkit
from email.message import EmailMessage
import smtplib
from twilio.rest import Client
import tweepy

# --- Add background image and overlay CSS for UI/UX consistency ---
st.markdown("""
<style>
body, .stApp {
    background-image: linear-gradient(rgba(30,30,30,0.85), rgba(30,30,30,0.85)), url('https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=1500&q=80');
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)

def python_automation_section(sub_choice=None):
    st.header(" Python Automation")

    if sub_choice == "Send Whatsap msg":
        with st.form("send_whatsapp_form"):
            st.subheader("Send WhatsApp Message")
            phone = st.text_input("Enter phone number with country code (e.g. +919876543210)")
            message = st.text_area("Enter your message")
            hour = st.number_input("Hour (24h format)", min_value=0, max_value=23)
            minute = st.number_input("Minute", min_value=0, max_value=59)
            submitted = st.form_submit_button("Send Message")
            if submitted:
                try:
                    pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute))
                    st.success("WhatsApp message scheduled successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif sub_choice == "Send E-mail":
        with st.form("send_email_form"):
            st.subheader("Send Email")
            sender = st.text_input("Sender Email")
            password = st.text_input("Email Password", type="password")
            receiver = st.text_input("Receiver Email")
            subject = st.text_input("Subject")
            body = st.text_area("Email Body")
            submitted = st.form_submit_button("Send Email")
            if submitted:
                try:
                    msg = EmailMessage()
                    msg.set_content(body)
                    msg['Subject'] = subject
                    msg['From'] = sender
                    msg['To'] = receiver
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender, password)
                        smtp.send_message(msg)
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif sub_choice == "Send Text msg":
        with st.form("send_sms_form"):
            st.subheader("Send SMS (Text Message)")
            st.warning("Requires Twilio account and credentials")
            account_sid = st.text_input("Twilio Account SID")
            auth_token = st.text_input("Auth Token", type="password")
            from_number = st.text_input("Twilio Phone Number (e.g., +12025550123)")
            to_number = st.text_input("Recipient Number (e.g., +919876543210)")
            message = st.text_area("Message")
            submitted = st.form_submit_button("Send SMS")
            if submitted:
                try:
                    client = Client(account_sid, auth_token)
                    client.messages.create(body=message, from_=from_number, to=to_number)
                    st.success("SMS sent successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif sub_choice == "Make a Phone call":
        with st.form("make_call_form"):
            st.subheader("Make a Phone Call (Twilio)")
            st.warning("Requires Twilio account and verified phone number")
            account_sid = st.text_input("Twilio Account SID")
            auth_token = st.text_input("Auth Token", type="password")
            from_number = st.text_input("Twilio Number")
            to_number = st.text_input("Your Number")
            call_url = st.text_input("TwiML URL", value="http://demo.twilio.com/docs/voice.xml")
            submitted = st.form_submit_button("Call Now")
            if submitted:
                try:
                    client = Client(account_sid, auth_token)
                    client.calls.create(url=call_url, to=to_number, from_=from_number)
                    st.success("Call initiated successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif sub_choice == "Post on Linkedin":
        with st.form("linkedin_form"):
            st.subheader("LinkedIn Posting (Manual)")
            st.info("LinkedIn API requires approval. For now, copy-paste content manually.")
            post = st.text_area("Post Content")
            submitted = st.form_submit_button("Generate Preview")
            if submitted:
                st.success("Here's your post:")
                st.write(post)

    elif sub_choice == "Post on Twitter":
        with st.form("twitter_form"):
            st.subheader("Tweet Something")
            tweet = st.text_area("Compose your tweet")
            st.warning("Requires Twitter API credentials")
            api_key = st.text_input("API Key")
            api_secret = st.text_input("API Secret", type="password")
            access_token = st.text_input("Access Token")
            access_secret = st.text_input("Access Token Secret", type="password")
            submitted = st.form_submit_button("Post Tweet")
            if submitted:
                try:
                    auth = tweepy.OAuthHandler(api_key, api_secret)
                    auth.set_access_token(access_token, access_secret)
                    api = tweepy.API(auth)
                    api.update_status(tweet)
                    st.success("✅ Tweet posted!")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif sub_choice == "Post on Facebook":
        with st.form("facebook_form"):
            st.subheader("Facebook Post")
            st.warning("Facebook API requires Graph API token and app review.")
            post = st.text_area("What’s on your mind?")
            submitted = st.form_submit_button("Preview")
            if submitted:
                st.success("Preview:")
                st.write(post)

    elif sub_choice == "Post on Instagram":
        with st.form("instagram_form"):
            st.subheader("Instagram Post (Manual/Third-Party Tool Recommended)")
            st.warning("Instagram posting via API is restricted. Use tools like Instabot or Meta Graph API.")
            caption = st.text_area("Write your caption")
            submitted = st.form_submit_button("Preview")
            if submitted:
                st.info("Caption Preview:")
                st.write(caption)

    elif sub_choice == "Send watsap image":
        with st.form("send_whatsapp_img"):
            st.subheader("Send WhatsApp Image")
            phone = st.text_input("Phone Number (with country code)")
            image_path = st.text_input("Image Path (e.g., C:/path/to/image.jpg)")
            caption = st.text_input("Caption")
            time_hour = st.number_input("Hour", min_value=0, max_value=23)
            time_minute = st.number_input("Minute", min_value=0, max_value=59)
            submitted = st.form_submit_button("Send Image")
            if submitted:
                try:
                    pywhatkit.sendwhats_image(phone, image_path, caption, time_hour, time_minute)
                    st.success("Image sent successfully via WhatsApp!")
                except Exception as e:
                    st.error(f"Error: {e}")

    else:
        st.error("Unknown Python Task.")
