import streamlit as st
import requests

def javascript_tasks_section(task):
    st.header("🧪 JavaScript-Based Automation Tasks")
    if task == "Take Photo":
        st.markdown("""
        <h4>📸 Capture Photo from Webcam</h4>
        <video id="video" width="300" height="200" autoplay></video><br>
        <button onclick="takePhoto()">Take Photo</button><br><br>
        <canvas id="canvas" width="300" height="200"></canvas>
        <script>
        var video = document.getElementById('video');
        navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
            video.srcObject = stream;
        });
        function takePhoto() {
            var canvas = document.getElementById('canvas');
            var context = canvas.getContext('2d');
            context.drawImage(video, 0, 0, 300, 200);
        }
        </script>
        """, unsafe_allow_html=True)

    elif task == "Send Email via JS":
        st.markdown("""
        <h4>📤 Send Email Using EmailJS</h4>
        <script src="https://cdn.jsdelivr.net/npm/emailjs-com@2/dist/email.min.js"></script>
        <script>
        function sendEmail() {
            emailjs.init("YOUR_USER_ID");
            emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", {
                to_name: "User",
                from_name: "Website",
                message: "Hello from JavaScript"
            }).then(response => {
                alert("Email sent successfully!");
            }, error => {
                alert("Failed to send: " + JSON.stringify(error));
            });
        }
        </script>
        <button onclick="sendEmail()">Send Email</button>
        """, unsafe_allow_html=True)

    elif task == "Send Captured Photo via Email":
        st.markdown("🚧 *Use backend + EmailJS or upload captured image via API (under development)*")

    elif task == "Record Video and Send via Email":
        st.markdown("""
        <h4>🎥 Record Video</h4>
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
                alert("Recording done. Now send this via backend.");
            };
            mediaRecorder.start();
        }
        function stopRecording() {
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
        }
        </script>
        """, unsafe_allow_html=True)

    elif task == "Send WhatsApp Message":
        st.markdown("""
        <h4>📲 Send WhatsApp Message</h4>
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
        """, unsafe_allow_html=True)

    elif task == "Send SMS via JS":
        st.markdown("""
        <h4>📩 Send SMS (Requires Backend API like Twilio)</h4>
        <p>Use JavaScript `fetch()` to call a server-side API.</p>
        """)

    elif task == "Show Current Location":
        st.markdown("""
        <h4>📍 Your Geo Location</h4>
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
        """, unsafe_allow_html=True)

    elif task == "Google Maps Live View":
        st.markdown("""
        <h4>🗺️ Google Maps (India)</h4>
        <iframe src="https://www.google.com/maps?q=India&output=embed" width="100%" height="300"></iframe>
        """, unsafe_allow_html=True)

    elif task == "Route from My Location to Destination":
        st.markdown("""
        <h4>🚗 Show Route on Google Maps</h4>
        <p>Example: Plot route from current location to Jaipur</p>
        <iframe
        src="https://www.google.com/maps/dir/?api=1&origin=Current+Location&destination=Jaipur"
        width="100%" height="300"></iframe>
        """, unsafe_allow_html=True)

    elif task == "Nearby Grocery Stores":
        st.markdown("""
        <h4>🛒 Grocery Stores Near Me</h4>
        <iframe src="https://www.google.com/maps/search/grocery+stores+near+me" width="100%" height="300"></iframe>
        """, unsafe_allow_html=True)

    elif task == "Fetch Last Gmail Email Info":
        st.markdown("📬 *Gmail API access requires OAuth – backend & scopes setup needed.*")

    elif task == "Post to Social Media":
        st.markdown("""
        <h4>📣 Social Media Posting (Basic)</h4>
        <p>Use browser APIs or automation tools to pre-fill post data.</p>
        <p>Try <a href="https://twitter.com/intent/tweet?text=Hello%20World" target="_blank">Post Tweet</a></p>
        """)

    elif task == "Track Most Viewed Products":
        st.markdown("📈 Most viewed products will be tracked using frontend cookies/localStorage and displayed.")

    elif task == "Get IP and Location":
        if st.button("Get My IP"):
            ip_data = requests.get("https://ipinfo.io").json()
            ip = ip_data.get("ip", "Unknown")
            loc = ip_data.get("city", "") + ", " + ip_data.get("region", "") + ", " + ip_data.get("country", "")
            st.success(f"Your current IP address is {ip} and your location is {loc}.")
