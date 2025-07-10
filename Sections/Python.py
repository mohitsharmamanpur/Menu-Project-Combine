import streamlit as st

def python_automation_section(sub_choice=None):
    st.header("🐍 Python Automation")
    if sub_choice == "Send Whatsap msg":
        st.subheader("Send WhatsApp Message")
        phone = st.text_input("Enter phone number with country code (e.g. +919876543210)")
        message = st.text_area("Enter your message")
        hour = st.number_input("Hour (24h format)", min_value=0, max_value=23)
        minute = st.number_input("Minute", min_value=0, max_value=59)
        if st.button("Send Message"):
            import pywhatkit
            try:
                pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute))
                st.success("WhatsApp message scheduled successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif sub_choice == "Send E-mail":
        st.subheader("Send Email")
        sender = st.text_input("Sender Email")
        password = st.text_input("Email Password", type="password")
        receiver = st.text_input("Receiver Email")
        subject = st.text_input("Subject")
        body = st.text_area("Email Body")
        if st.button("Send Email"):
            import smtplib
            from email.message import EmailMessage
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
        st.subheader("Send SMS (Text Message)")
        st.warning("Requires Twilio account and credentials")
        account_sid = st.text_input("Twilio Account SID")
        auth_token = st.text_input("Auth Token", type="password")
        from_number = st.text_input("Twilio Phone Number (e.g., +12025550123)")
        to_number = st.text_input("Recipient Number (e.g., +919876543210)")
        message = st.text_area("Message")
        if st.button("Send SMS"):
            try:
                from twilio.rest import Client
                client = Client(account_sid, auth_token)
                client.messages.create(body=message, from_=from_number, to=to_number)
                st.success("SMS sent successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif sub_choice == "Make a Phone call":
        st.subheader("Make a Phone Call (Twilio)")
        st.warning("Requires Twilio account and verified phone number")
        account_sid = st.text_input("Twilio Account SID")
        auth_token = st.text_input("Auth Token", type="password")
        from_number = st.text_input("Twilio Number")
        to_number = st.text_input("Your Number")
        call_url = st.text_input("URL with TwiML instructions", value="http://demo.twilio.com/docs/voice.xml")
        if st.button("Call Now"):
            try:
                from twilio.rest import Client
                client = Client(account_sid, auth_token)
                call = client.calls.create(url=call_url, to=to_number, from_=from_number)
                st.success("Call initiated successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif sub_choice == "Post on Linkedin":
        st.subheader("LinkedIn Posting (Manual)")
        st.info("LinkedIn API requires approval. For now, copy-paste content manually.")
        post = st.text_area("Post Content")
        if st.button("Generate Preview"):
            st.success("Here's your post:")
            st.write(post)

    elif sub_choice == "Post on Twitter":
        st.subheader("Tweet Something")
        tweet = st.text_area("Compose your tweet")
        st.warning("Requires Twitter API credentials")
        if st.button("Post Tweet"):
            try:
                import tweepy
                api_key = st.text_input("API Key")
                api_secret = st.text_input("API Secret", type="password")
                access_token = st.text_input("Access Token")
                access_secret = st.text_input("Access Token Secret", type="password")
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_secret)
                api = tweepy.API(auth)
                api.update_status(tweet)
                st.success("✅ Tweet posted!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif sub_choice == "Post on Facebook":
        st.subheader("Facebook Post")
        st.warning("Facebook API requires Graph API token and app review.")
        post = st.text_area("What’s on your mind?")
        if st.button("Preview"):
            st.success("Preview:")
            st.write(post)

    elif sub_choice == "Post on Instagram":
        st.subheader("Instagram Post (Manual/Third-Party Tool Recommended)")
        st.warning("Instagram posting via API is restricted. Use tools like Instabot or Meta Graph API.")
        caption = st.text_area("Write your caption")
        if st.button("Preview"):
            st.info("Caption Preview:")
            st.write(caption)

    elif sub_choice == "Send watsap image":
        st.subheader("Send WhatsApp Image")
        phone = st.text_input("Phone Number (with country code)")
        image_path = st.text_input("Image Path (full path on system)")
        caption = st.text_input("Caption")
        time_hour = st.number_input("Hour", min_value=0, max_value=23)
        time_minute = st.number_input("Minute", min_value=0, max_value=59)
        if st.button("Send Image"):
            try:
                import pywhatkit
                pywhatkit.sendwhats_image(phone, image_path, caption, time_hour, time_minute)
                st.success("Image sent successfully via WhatsApp!")
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.error("Unknown Python Task.")
