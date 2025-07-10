import streamlit as st
import os
import datetime
import pyttsx3
import pyautogui
import pyjokes
import pywhatkit
import smtplib
import psutil
import cv2

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def windows_section():
    st.header("🪟 Windows Assistant")
    user_input = st.text_input("💬 Enter your command:")

    if st.button("▶️ Run Command"):
        user_input = user_input.lower()

        if "notepad" in user_input:
            os.system("notepad")

        elif "hii" in user_input or "kya haal h" in user_input:
            speak("Hello bhai, tu bta kesa h")

        elif "badia hu bhai" in user_input or "ek dum mast" in user_input or "shandar" in user_input or "badia" in user_input:
            speak("OK bhai, All the best")

        elif "date" in user_input or "taarik" in user_input or "tarik" in user_input:
            speak(f"Today's date is {datetime.datetime.now().strftime('%d %B %Y')}")

        elif "calendar" in user_input:
            speak("Windows doesn't have terminal calendar. Please open it manually.")

        elif "list" in user_input or "files" in user_input:
            os.system("dir")

        elif "directory" in user_input or "path" in user_input:
            os.system("cd")

        elif "ip" in user_input or "ip" in user_input:
            os.system("ipconfig")

        elif "user" in user_input:
            os.system("whoami")

        elif "process" in user_input or "running" in user_input:
            os.system("tasklist")

        elif "whatsapp image" in user_input or "message" in user_input or "msg" in user_input:
            speak("Please type the number, message, and time for WhatsApp")
            number = st.text_input("📱 Enter phone number with country code:")
            message = st.text_input("💬 Enter the message:")
            hour = st.number_input("🕐 Enter hour (24-hour format):", min_value=0, max_value=23)
            minute = st.number_input("🕒 Enter minute:", min_value=0, max_value=59)
            if st.button("📩 Schedule WhatsApp Message"):
                speak("Scheduling your message...")
                pywhatkit.sendwhatmsg(number, message, int(hour), int(minute))
                speak("Message scheduled successfully!")

        elif "watsap image" in user_input or "image" in user_input:
            speak("Please type the number, image path, text and time")
            number = st.text_input("📱 Enter phone number:")
            image_path = st.text_input("🖼️ Enter image path:")
            caption = st.text_input("📝 Enter caption text:")
            wait_time = st.number_input("⏱️ Enter wait time (in seconds):", min_value=1)
            if st.button("📤 Send WhatsApp Image"):
                speak("Sending image to WhatsApp, please wait...")
                pywhatkit.sendwhats_image(number, image_path, caption, int(wait_time))
                speak("Image sent successfully.")

        elif "send email" in user_input:
            message = st.text_area("📧 Enter the email message:")
            to = st.text_input("📨 Recipient Email:")
            if st.button("📬 Send Email"):
                try:
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login('your_email@gmail.com', 'your_app_password')  # Replace!
                    server.sendmail('your_email@gmail.com', to, message)
                    server.quit()
                    speak("Email sent successfully.")
                except:
                    st.error("Failed to send email. Check credentials.")

        elif "google" in user_input:
            os.system("start https://www.google.com")

        elif "youtube" in user_input:
            os.system("start https://www.youtube.com")

        elif "search" in user_input:
            speak("What do you want to search?")
            query = st.text_input("🔎 Enter search query:")
            if st.button("Search"):
                pywhatkit.search(query)

        elif "play" in user_input or "song" in user_input:
            song = st.text_input("🎵 Enter song name to play on YouTube:")
            if st.button("▶️ Play Song"):
                pywhatkit.playonyt(song)

        elif "internet speed" in user_input or "net speed" in user_input:
            os.system("start https://fast.com")

        elif "shutdown" in user_input:
            speak("Shutting down your system in 5 seconds.")
            os.system("shutdown /s /t 5")

        elif "restart" in user_input:
            speak("Restarting your system in 5 seconds.")
            os.system("shutdown /r /t 5")

        elif "create folder" in user_input or "make folder" in user_input:
            folder_name = st.text_input("📁 Enter folder name:")
            if st.button("📂 Create Folder"):
                os.system(f"mkdir {folder_name}")
                speak(f"Folder '{folder_name}' created successfully.")

        elif "delete folder" in user_input or "remove folder" in user_input:
            folder_name = st.text_input("🗑️ Enter folder name to delete:")
            if st.button("❌ Delete Folder"):
                os.system(f"rmdir /s /q {folder_name}")
                speak(f"Folder '{folder_name}' deleted.")

        elif "open downloads" in user_input:
            os.startfile(os.path.expanduser("~/Downloads"))

        elif "open desktop" in user_input:
            os.startfile(os.path.expanduser("~/Desktop"))

        elif "open documents" in user_input:
            os.startfile(os.path.expanduser("~/Documents"))

        elif "open facebook" in user_input:
            os.system("start https://www.facebook.com")

        elif "open instagram" in user_input:
            os.system("start https://www.instagram.com")

        elif "open twitter" in user_input or "open x" in user_input:
            os.system("start https://twitter.com")

        elif "open github" in user_input:
            os.system("start https://github.com")

        elif "open gmail" in user_input or "check mail" in user_input:
            os.system("start https://mail.google.com")

        elif "open linkedin" in user_input:
            os.system("start https://www.linkedin.com")
            speak("Opening LinkedIn.")

        elif "calculator" in user_input:
            os.system("calc")

        elif "screenshot" in user_input:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot taken and saved as screenshot.png")

        elif "battery" in user_input or "battery status" in user_input:
            battery = psutil.sensors_battery()
            percent = battery.percent
            speak(f"Battery is at {percent} percent")

        elif "time" in user_input:
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Current time is {now}")

        elif "write a note" in user_input or "take a note" in user_input:
            note = st.text_area("📝 What should I write?")
            if st.button("✍️ Save Note"):
                with open("note.txt", "a") as f:
                    f.write(note + "\n")
                speak("Note written successfully.")

        elif "read notes" in user_input:
            try:
                with open("note.txt", "r") as f:
                    notes = f.read()
                    speak("Here are your notes.")
                    st.text_area("📖 Your Notes", notes, height=200)
            except FileNotFoundError:
                speak("You don't have any saved notes.")

        elif "who made you" in user_input or "who created you" in user_input:
            speak("I was created by team 37 during their internship. I am learning new skills every day!")

        elif "joke" in user_input:
            joke = pyjokes.get_joke()
            speak(joke)
            st.success(joke)

        elif "thank you" in user_input:
            speak("You're welcome bhai!")

        elif "how are you" in user_input:
            speak("I'm fine, just chilling inside your processor!")

        elif "open camera" in user_input:
            cam = cv2.VideoCapture(0)
            while True:
                ret, frame = cam.read()
                cv2.imshow("Camera", frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            cam.release()
            cv2.destroyAllWindows()

        elif "exit" in user_input or "quit" in user_input:
            speak("Exiting... Good bye!")
            st.stop()

        elif user_input == "":
            st.warning("Please enter a command.")

        else:
            speak("Sorry, I don't understand that command.")
