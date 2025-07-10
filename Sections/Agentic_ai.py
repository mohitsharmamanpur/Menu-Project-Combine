import streamlit as st

def agentic_ai_section(sub_choice=None):
    st.header(" Agentic AI")
    st.info(f"Selected: {sub_choice}")
    chatbot_option = st.selectbox("Select Chatbot Version", [
        "Chatbot 1 - Gemini Finance Bot",
        "Chatbot 2 - FAQ Bot",
        "Chatbot 3 - Sentiment-Aware",
        "Chatbot 4 - Generative AI"
    ])

    if chatbot_option == "Chatbot 1 - Gemini Finance Bot":
        st.markdown("### Ask me anything about **Stock Market & Finance**")
        import google.generativeai as genai
        genai.configure(api_key="AIzaSyABUqgYzp7ekmlyKErgG5hu_-H0JIAPB1A")
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        def finance_bot(question):
            try:
                prompt = f"You are a finance education assistant. Explain this in simple words:\n\n{question}"
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                return f"Error: {str(e)}"

        question = st.text_input("Enter your finance-related question", placeholder="e.g., What is SIP?")
        if st.button("Get Answer"):
            if question.strip():
                answer = finance_bot(question)
                st.success("Gemini's Answer:")
                st.write(answer)
            else:
                st.warning("Please enter a question first.")

        st.markdown("#### Try an example:")
        example = st.selectbox("Example Questions", [
            "",
            "What is SIP?",
            "Difference between stocks and mutual funds",
            "Explain compound interest",
            "What is Nifty 50?",
            "Best books to learn investing"
        ])
        if example:
            st.info(f"Gemini's Answer to: {example}")
            st.write(finance_bot(example))

    elif chatbot_option == "Chatbot 2 - FAQ Bot":
        st.write("Chatbot 2: Answering FAQs... (Coming soon)")

    elif chatbot_option == "Chatbot 3 - Sentiment-Aware":
        st.write("Chatbot 3: Detecting your emotion and responding accordingly... (Coming soon)")

    elif chatbot_option == "Chatbot 4 - Generative AI":
        st.write("Chatbot 4: Generating AI-based dynamic response... (Coming soon)")

    else:
        st.error("Invalid chatbot selected.")
