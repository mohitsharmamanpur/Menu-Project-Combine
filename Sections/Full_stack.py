import streamlit as st
import requests

def take_photo():
    st.markdown("""
    <h3>📸 Take Photo</h3>
    <script>
    async function capturePhoto() {
        const video = document.createElement("video");
        document.body.append(video);
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        await video.play();
        const canvas = document.createElement("canvas");
        canvas.width = 300;
        canvas.height = 250;
        const context = canvas.getContext("2d");
        context.drawImage(video, 0, 0, 300, 250);
        const dataURL = canvas.toDataURL("image/png");
        fetch("/", {
            method: "POST",
            body: dataURL
        });
        stream.getTracks().forEach(track => track.stop());
    }
    </script>
    <button onclick="capturePhoto()">Capture</button>
    """, unsafe_allow_html=True)

def send_email():
    st.markdown("📧 **Send Email Feature Placeholder**")
    st.info("Use SendGrid API or SMTP for actual implementation.")

def send_photo_email():
    st.markdown("📤 **Send Captured Photo via Email** (Requires Backend Storage/API)")
    st.warning("Capture + Email requires server-side integration.")

def record_video_send_email():
    st.markdown("""
    🎥 **Record Video** (HTML5 + JS Example - Demo)
    <video id="recVid" autoplay muted></video><br>
    <button onclick="navigator.mediaDevices.getUserMedia({video:true}).then(s=>{recVid.srcObject=s})">Record</button>
    """, unsafe_allow_html=True)

def send_whatsapp():
    st.markdown("📲 **Send WhatsApp Message** (Twilio API recommended)")
    st.code("twilio.messages.create(from_, to, body='Hello!')", language="python")

def send_sms():
    st.markdown("📩 **Send SMS using API** (Nexmo/Twilio required)")
    st.code("requests.post('https://api.twilio.com', data=...)", language="python")

def show_location():
    st.markdown("""
    🌐 **Current Location**
    <button onclick="navigator.geolocation.getCurrentPosition(pos => alert(`Lat: ${pos.coords.latitude}, Lon: ${pos.coords.longitude}`))">Get My Location</button>
    """, unsafe_allow_html=True)

def show_map():
    st.markdown("""
    🗺️ **Google Map Live**
    <iframe src="https://maps.google.com/maps?q=India&t=&z=13&ie=UTF8&iwloc=&output=embed"
    width="100%" height="300" style="border:0;"></iframe>
    """, unsafe_allow_html=True)

def show_route():
    st.markdown("🚗 **Show Route on Google Maps**")
    st.markdown("Use Google Maps Directions API with origin and destination.")

def show_grocery():
    st.markdown("🛒 **Nearby Grocery Stores**")
    st.markdown("""
    <iframe
      src="https://www.google.com/maps/search/grocery+store+near+me"
      width="100%" height="300" style="border:0;"></iframe>
    """, unsafe_allow_html=True)

def fetch_email():
    st.markdown("📬 **Fetch Last Email from Gmail**")
    st.info("Use Gmail API with OAuth2 for full access.")

def social_media_post():
    st.markdown("📣 **Post to Social Media**")
    st.info("Use Meta Graph API or open new tab with prefilled data.")

def product_tracking():
    st.markdown("🔥 **Recommended Products**")
    st.json({"Most Viewed": ["iPhone", "Echo Dot", "MacBook"]})

def ip_location():
    st.markdown("📍 **Your IP and Location**")
    if st.button("Get My IP"):
        ip_data = requests.get("https://ipinfo.io").json()
        st.write(ip_data)

def full_stack_section():
    st.header("🖥️ Full-Stack Components")

    task = st.selectbox("Choose Fullstack Task", [
        "Take Photo", "Send Email", "Send Photo to Email", "Record Video + Email", "Send WhatsApp",
        "Send SMS", "Show Location", "Google Maps View", "Route to Destination", "Nearby Grocery",
        "Fetch Gmail", "Social Post", "Track Products", "Get IP"])

    if task == "Take Photo":
        take_photo()
    elif task == "Send Email":
        send_email()
    elif task == "Send Photo to Email":
        send_photo_email()
    elif task == "Record Video + Email":
        record_video_send_email()
    elif task == "Send WhatsApp":
        send_whatsapp()
    elif task == "Send SMS":
        send_sms()
    elif task == "Show Location":
        show_location()
    elif task == "Google Maps View":
        show_map()
    elif task == "Route to Destination":
        show_route()
    elif task == "Nearby Grocery":
        show_grocery()
    elif task == "Fetch Gmail":
        fetch_email()
    elif task == "Social Post":
        social_media_post()
    elif task == "Track Products":
        product_tracking()
    elif task == "Get IP":
        ip_location()
