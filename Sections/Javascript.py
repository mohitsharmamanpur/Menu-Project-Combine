import streamlit as st
import requests
import streamlit.components.v1 as components

def javascript_tasks_section(task):
    st.header("🧪 JavaScript-Based Automation Tasks")

    if task == "Take Photo":
        st.subheader("📸 Capture Photo from Webcam")
        components.html("""
        <video id="video" width="300" height="200" autoplay></video><br>
        <button onclick="takePhoto()">Take Photo</button><br><br>
        <canvas id="canvas" width="300" height="200"></canvas>
        <script>
        var video = document.getElementById('video');
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
            video.srcObject = stream;
        });
        function takePhoto() {
            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, 300, 200);
        }
        </script>
        """, height=400)

    elif task == "Send Email via JS":
        st.subheader("📤 Send Email Using EmailJS")
        st.info("Requires EmailJS credentials. Not supported natively in Streamlit.")
        components.html("""
        <script src="https://cdn.jsdelivr.net/npm/emailjs-com@2/dist/email.min.js"></script>
        <button onclick="sendEmail()">Send Email</button>
        <script>
        function sendEmail() {
            emailjs.init("YOUR_USER_ID");
            emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", {
                to_name: "User",
                from_name: "Website",
                message: "Hello from JavaScript"
            }).then(function(response) {
                alert("Email sent!");
            }, function(error) {
                alert("Failed: " + JSON.stringify(error));
            });
        }
        </script>
        """, height=150)

    elif task == "Send Captured Photo via Email":
        st.subheader("🚧 Send Captured Photo via Email")
        st.warning("This feature requires custom backend + EmailJS + file upload (not supported in-browser alone).")

    elif task == "Record Video and Send via Email":
        st.subheader("🎥 Record Video from Webcam")
        components.html("""
        <video id="recVid" autoplay muted></video><br>
        <button onclick="startRecording()">Start</button>
        <button onclick="stopRecording()">Stop</button>
        <script>
        let mediaRecorder, stream, chunks = [];
        async function startRecording() {
            stream = await navigator.mediaDevices.getUserMedia({ video: true });
            document.getElementById('recVid').srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = e => chunks.push(e.data);
            mediaRecorder.onstop = () => {
                let blob = new Blob(chunks, { type: 'video/webm' });
                alert("Recording done. Send video via backend.");
            };
            mediaRecorder.start();
        }
        function stopRecording() {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        }
        </script>
        """, height=350)

    elif task == "Send WhatsApp Message":
        st.subheader("📲 Send WhatsApp Message")
        components.html("""
        <input type="text" id="w_phone" placeholder="+91XXXXXXXXXX">
        <input type="text" id="w_msg" placeholder="Your message"><br><br>
        <button onclick="sendWAMsg()">Send via WhatsApp</button>
        <script>
        function sendWAMsg() {
            let phone = document.getElementById('w_phone').value;
            let msg = document.getElementById('w_msg').value;
            let url = `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
            window.open(url, "_blank");
        }
        </script>
        """, height=150)

    elif task == "Send SMS via JS":
        st.subheader("📩 Send SMS via JS")
        st.warning("Requires a backend API like Twilio or FastAPI. Use fetch() in JavaScript to call server.")

    elif task == "Show Current Location":
        st.subheader("📍 Your Geo Location")
        components.html("""
        <button onclick="getLocation()">Get My Location</button>
        <p id="geo"></p>
        <script>
        function getLocation() {
            navigator.geolocation.getCurrentPosition(position => {
                let msg = "Latitude: " + position.coords.latitude + ", Longitude: " + position.coords.longitude;
                document.getElementById("geo").innerText = msg;
            });
        }
        </script>
        """, height=200)

    elif task == "Google Maps Live View":
        st.subheader("🗺️ Google Maps (India)")
        components.html("""
        <iframe src="https://www.google.com/maps?q=India&output=embed" width="100%" height="300"></iframe>
        """, height=300)

    elif task == "Route from My Location to Destination":
        st.subheader("🚗 Route to Jaipur from Current Location")
        components.html("""
        <iframe
        src="https://www.google.com/maps/dir/?api=1&origin=Current+Location&destination=Jaipur"
        width="100%" height="300"></iframe>
        """, height=300)

    elif task == "Nearby Grocery Stores":
        st.subheader("🛒 Grocery Stores Near Me")
        try:
            ip_info = requests.get("https://ipinfo.io").json()
            loc = ip_info.get("loc")  # Format: "latitude,longitude"
            if loc:
                latitude, longitude = loc.split(",")
                map_url = f"https://www.google.com/maps/search/grocery+stores/@{latitude},{longitude},15z"
                components.html(f"""
                <iframe src="{map_url}" width="100%" height="300"></iframe>
                """, height=300)
            else:
                st.error("Could not fetch location.")
        except Exception as e:
            st.error(f"Failed to load map: {e}")

    elif task == "Fetch Last Gmail Email Info":
        st.subheader("📬 Fetch Gmail Info")
        st.warning("Gmail API requires OAuth2 scopes and backend support.")

    elif task == "Post to Social Media":
        st.subheader("📣 Post to Social Media")
        st.markdown("""
        - [🕊️ Post a Tweet](https://twitter.com/intent/tweet?text=Hello%20World)  
        - [📘 Post to Facebook](https://facebook.com)  
        - [📸 Post to Instagram](https://instagram.com)
        """)

    elif task == "Track Most Viewed Products":
        st.subheader("📈 Track Most Viewed Products")
        st.info("This can be done using cookies or localStorage via frontend JS. Streamlit cannot handle it directly.")

    elif task == "Get IP and Location":
        st.subheader("🌐 Your IP & Location Info")
        if st.button("Get My IP"):
            try:
                ip_data = requests.get("https://ipinfo.io").json()
                ip = ip_data.get("ip", "Unknown")
                loc = f"{ip_data.get('city', '')}, {ip_data.get('region', '')}, {ip_data.get('country', '')}"
                st.success(f"IP Address: {ip}\nLocation: {loc}")
            except:
                st.error("Unable to fetch IP information. Try again later.")
