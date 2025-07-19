import streamlit as st
import openai
import google.generativeai as genai
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import requests

def log_command(command):
    """Log command to file"""
    with open("command_log.txt", "a") as f:
        f.write(f"{datetime.now()}: {command}\n")

def agentic_ai_section(sub_choice=None):
    st.markdown('<h1 class="section-header">🤖 Agentic AI Platform</h1>', unsafe_allow_html=True)
    
    # AI Configuration
    st.subheader("🔧 AI Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        openai_api_key = st.text_input("OpenAI API Key:", type="password")
        if openai_api_key:
            st.session_state.openai_api_key = openai_api_key
            openai.api_key = openai_api_key
    
    with col2:
        gemini_api_key = st.text_input("Gemini API Key:", type="password")
        if gemini_api_key:
            st.session_state.gemini_api_key = gemini_api_key
            genai.configure(api_key=gemini_api_key)
    
    # Model selection
    ai_model = st.selectbox("Select AI Model:", [
        "OpenAI GPT-4", "OpenAI GPT-3.5-turbo", "Gemini Pro", "Gemini Flash"
    ])
    
    if sub_choice == "💬 Chatbot":
        chatbot_section(ai_model)
    elif sub_choice == "📄 Document Q&A":
        document_qa_section(ai_model)
    elif sub_choice == "📝 AI Summarizer":
        ai_summarizer_section(ai_model)
    elif sub_choice == "🎯 Task Executor":
        task_executor_section(ai_model)
    else:
        st.info("Please select an AI feature from the sidebar.")

def chatbot_section(ai_model):
    st.subheader("💬 AI Chat Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI is thinking..."):
                try:
                    if "OpenAI" in ai_model:
                        if not st.session_state.get('openai_api_key'):
                            st.error("Please provide OpenAI API key")
                            return
                        
                        if "GPT-4" in ai_model:
                            model_name = "gpt-4"
                        else:
                            model_name = "gpt-3.5-turbo"
                        
                        response = openai.ChatCompletion.create(
                            model=model_name,
                            messages=[
                                {"role": "system", "content": "You are a helpful AI assistant. Provide clear, accurate, and helpful responses."},
                                {"role": "user", "content": prompt}
                            ],
                            max_tokens=1000,
                            temperature=0.7
                        )
                        ai_response = response.choices[0].message.content
                    
                    elif "Gemini" in ai_model:
                        if not st.session_state.get('gemini_api_key'):
                            st.error("Please provide Gemini API key")
                            return
                        
                        if "Pro" in ai_model:
                            model = genai.GenerativeModel("gemini-pro")
                        else:
                            model = genai.GenerativeModel("gemini-1.5-flash")
                        
                        response = model.generate_content(prompt)
                        ai_response = response.text
                    
                    else:
                        ai_response = "Model not configured properly."
                    
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    log_command(f"AI Chat: Generated response using {ai_model}")
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
    
    # Chat controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("💾 Save Chat"):
            if st.session_state.messages:
                chat_data = {
                    "timestamp": datetime.now().isoformat(),
                    "model": ai_model,
                    "messages": st.session_state.messages
                }
                with open(f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
                    json.dump(chat_data, f, indent=2)
                st.success("Chat saved!")
    
    with col3:
        if st.button("📊 Chat Stats"):
            if st.session_state.messages:
                user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
                ai_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
                st.metric("User Messages", user_messages)
                st.metric("AI Responses", ai_messages)

def document_qa_section(ai_model):
    st.subheader("📄 Document Q&A System")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a document (PDF, TXT, DOCX)", 
        type=['txt', 'pdf', 'docx'],
        help="Upload a document to ask questions about its content"
    )
    
    if uploaded_file is not None:
        # Read document content
        try:
            if uploaded_file.type == "text/plain":
                document_content = str(uploaded_file.read(), "utf-8")
            else:
                # For PDF and DOCX, you'd need additional libraries
                st.warning("PDF and DOCX support coming soon. Please upload a TXT file.")
                document_content = ""
            
            if document_content:
                st.success(f"✅ Document loaded: {uploaded_file.name}")
                st.session_state.document_content = document_content
                
                # Show document preview
                with st.expander("📄 Document Preview"):
                    st.text(document_content[:1000] + "..." if len(document_content) > 1000 else document_content)
                
                # Q&A interface
                st.subheader("❓ Ask Questions About the Document")
                
                question = st.text_input("Enter your question:", placeholder="What is the main topic of this document?")
                
                if st.button("🔍 Get Answer"):
                    if question and st.session_state.get('document_content'):
                        with st.spinner("🤖 Analyzing document..."):
                            try:
                                # Create context-aware prompt
                                context = st.session_state.document_content[:3000]  # Limit context size
                                prompt = f"""Based on the following document content, please answer this question: {question}

Document Content:
{context}

Please provide a clear and accurate answer based only on the information in the document."""
                                
                                if "OpenAI" in ai_model:
                                    if not st.session_state.get('openai_api_key'):
                                        st.error("Please provide OpenAI API key")
                                        return
                                    
                                    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "system", "content": "You are a helpful assistant that answers questions based on provided document content."},
                                            {"role": "user", "content": prompt}
                                        ],
                                        max_tokens=500,
                                        temperature=0.3
                                    )
                                    answer = response.choices[0].message.content
                                
                                elif "Gemini" in ai_model:
                                    if not st.session_state.get('gemini_api_key'):
                                        st.error("Please provide Gemini API key")
                                        return
                                    
                                    model = genai.GenerativeModel("gemini-pro")
                                    response = model.generate_content(prompt)
                                    answer = response.text
                                
                                else:
                                    answer = "Model not configured properly."
                                
                                st.success("📄 Answer:")
                                st.write(answer)
                                log_command(f"Document Q&A: Answered question about {uploaded_file.name}")
                                
                            except Exception as e:
                                st.error(f"Error generating answer: {e}")
                
                # Multiple questions
                st.subheader("📋 Batch Questions")
                questions_text = st.text_area(
                    "Enter multiple questions (one per line):",
                    placeholder="What is the main topic?\nWho is the author?\nWhat are the key points?"
                )
                
                if st.button("🔍 Answer All Questions"):
                    if questions_text and st.session_state.get('document_content'):
                        questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
                        
                        with st.spinner(f"🤖 Answering {len(questions)} questions..."):
                            for i, question in enumerate(questions, 1):
                                st.write(f"**Q{i}: {question}**")
                                
                                try:
                                    context = st.session_state.document_content[:3000]
                                    prompt = f"Based on this document content, answer: {question}\n\nDocument: {context}"
                                    
                                    if "OpenAI" in ai_model:
                                        response = openai.ChatCompletion.create(
                                            model="gpt-3.5-turbo",
                                            messages=[{"role": "user", "content": prompt}],
                                            max_tokens=200,
                                            temperature=0.3
                                        )
                                        answer = response.choices[0].message.content
                                    elif "Gemini" in ai_model:
                                        model = genai.GenerativeModel("gemini-pro")
                                        response = model.generate_content(prompt)
                                        answer = response.text
                                    else:
                                        answer = "Model not configured."
                                    
                                    st.write(f"**A{i}:** {answer}")
                                    st.divider()
                                    
                                except Exception as e:
                                    st.error(f"Error answering question {i}: {e}")
                        
                        log_command(f"Document Q&A: Answered {len(questions)} questions about {uploaded_file.name}")
        
        except Exception as e:
            st.error(f"Error reading document: {e}")

def ai_summarizer_section(ai_model):
    st.subheader("📝 AI Text Summarizer")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["📝 Text Input", "📄 File Upload"])
    
    if input_method == "📝 Text Input":
        text_content = st.text_area(
            "Enter text to summarize:",
            height=200,
            placeholder="Paste your text here..."
        )
        
        if text_content:
            st.session_state.text_to_summarize = text_content
    else:
        uploaded_file = st.file_uploader("Upload a text file", type=['txt'])
        if uploaded_file:
            try:
                text_content = str(uploaded_file.read(), "utf-8")
                st.session_state.text_to_summarize = text_content
                st.success(f"✅ File loaded: {uploaded_file.name}")
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    # Summarization options
    if st.session_state.get('text_to_summarize'):
        st.subheader("🔧 Summarization Options")
        
        col1, col2 = st.columns(2)
        with col1:
            summary_length = st.selectbox("Summary Length:", ["Short", "Medium", "Long"])
            summary_style = st.selectbox("Summary Style:", ["Bullet Points", "Paragraph", "Executive Summary"])
        
        with col2:
            focus_areas = st.multiselect("Focus Areas:", [
                "Key Points", "Main Arguments", "Conclusions", "Recommendations", "Facts & Figures"
            ])
            include_quotes = st.checkbox("Include Key Quotes")
        
        if st.button("📝 Generate Summary"):
            text = st.session_state.text_to_summarize
            
            with st.spinner("🤖 Generating summary..."):
                try:
                    # Create summarization prompt
                    length_map = {"Short": "100 words", "Medium": "200 words", "Long": "300 words"}
                    style_map = {
                        "Bullet Points": "as bullet points",
                        "Paragraph": "as a coherent paragraph",
                        "Executive Summary": "as an executive summary"
                    }
                    
                    prompt = f"""Please summarize the following text in {length_map[summary_length]} {style_map[summary_style]}.

Text to summarize:
{text[:4000]}  # Limit text length

Focus on: {', '.join(focus_areas) if focus_areas else 'all important information'}
Include key quotes: {'Yes' if include_quotes else 'No'}

Please provide a clear, well-structured summary."""
                    
                    if "OpenAI" in ai_model:
                        if not st.session_state.get('openai_api_key'):
                            st.error("Please provide OpenAI API key")
                            return
                        
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=500,
                            temperature=0.3
                        )
                        summary = response.choices[0].message.content
                    
                    elif "Gemini" in ai_model:
                        if not st.session_state.get('gemini_api_key'):
                            st.error("Please provide Gemini API key")
                            return
                        
                        model = genai.GenerativeModel("gemini-pro")
                        response = model.generate_content(prompt)
                        summary = response.text
                    
                    else:
                        summary = "Model not configured properly."
                    
                    st.success("📝 Summary Generated:")
                    st.write(summary)
                    
                    # Summary statistics
                    original_words = len(text.split())
                    summary_words = len(summary.split())
                    compression_ratio = (1 - summary_words / original_words) * 100
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Original Words", original_words)
                    col2.metric("Summary Words", summary_words)
                    col3.metric("Compression", f"{compression_ratio:.1f}%")
                    
                    log_command(f"AI Summarizer: Generated {summary_length} summary using {ai_model}")
                    
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

def task_executor_section(ai_model):
    st.subheader("🎯 AI Task Executor")
    
    # Task categories
    task_category = st.selectbox("Select Task Category:", [
        "📊 Data Analysis", "📝 Content Creation", "🔍 Research Assistant", "💻 Code Generation", "📈 Business Analysis"
    ])
    
    if task_category == "📊 Data Analysis":
        st.subheader("📊 AI Data Analysis")
        
        # Data input
        data_input = st.text_area(
            "Enter your data or describe what you want to analyze:",
            placeholder="Paste CSV data, describe a dataset, or ask for analysis..."
        )
        
        analysis_type = st.selectbox("Analysis Type:", [
            "Descriptive Statistics", "Trend Analysis", "Correlation Analysis", "Outlier Detection", "Pattern Recognition"
        ])
        
        if st.button("🔍 Analyze Data"):
            if data_input:
                with st.spinner("🤖 Analyzing data..."):
                    try:
                        prompt = f"""You are a data analyst. Please perform {analysis_type} on the following data:

Data/Description: {data_input}

Please provide:
1. Key insights and findings
2. Relevant statistics or patterns
3. Recommendations based on the analysis
4. Visual suggestions (if applicable)

Format your response clearly with sections."""
                        
                        if "OpenAI" in ai_model:
                            if not st.session_state.get('openai_api_key'):
                                st.error("Please provide OpenAI API key")
                                return
                            
                            response = openai.ChatCompletion.create(
                                model="gpt-4" if "GPT-4" in ai_model else "gpt-3.5-turbo",
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=800,
                                temperature=0.3
                            )
                            analysis = response.choices[0].message.content
                        
                        elif "Gemini" in ai_model:
                            if not st.session_state.get('gemini_api_key'):
                                st.error("Please provide Gemini API key")
                                return
                            
                            model = genai.GenerativeModel("gemini-pro")
                            response = model.generate_content(prompt)
                            analysis = response.text
                        
                        else:
                            analysis = "Model not configured properly."
                        
                        st.success("📊 Analysis Results:")
                        st.write(analysis)
                        log_command(f"AI Task: Performed {analysis_type} using {ai_model}")
                        
                    except Exception as e:
                        st.error(f"Error performing analysis: {e}")
    
    elif task_category == "📝 Content Creation":
        st.subheader("📝 AI Content Creator")
        
        content_type = st.selectbox("Content Type:", [
            "Blog Post", "Email", "Social Media Post", "Report", "Creative Story", "Technical Documentation"
        ])
        
        topic = st.text_input("Topic or Title:")
        tone = st.selectbox("Tone:", ["Professional", "Casual", "Academic", "Creative", "Technical"])
        length = st.selectbox("Length:", ["Short", "Medium", "Long"])
        
        if st.button("✍️ Generate Content"):
            if topic:
                with st.spinner("🤖 Creating content..."):
                    try:
                        prompt = f"""Create a {content_type.lower()} about "{topic}".

Requirements:
- Tone: {tone}
- Length: {length}
- Make it engaging and informative
- Include relevant details and examples

Please provide well-structured, high-quality content."""
                        
                        if "OpenAI" in ai_model:
                            if not st.session_state.get('openai_api_key'):
                                st.error("Please provide OpenAI API key")
                                return
                            
                            response = openai.ChatCompletion.create(
                                model="gpt-4" if "GPT-4" in ai_model else "gpt-3.5-turbo",
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=1000,
                                temperature=0.7
                            )
                            content = response.choices[0].message.content
                        
                        elif "Gemini" in ai_model:
                            if not st.session_state.get('gemini_api_key'):
                                st.error("Please provide Gemini API key")
                                return
                            
                            model = genai.GenerativeModel("gemini-pro")
                            response = model.generate_content(prompt)
                            content = response.text
                        
                        else:
                            content = "Model not configured properly."
                        
                        st.success("📝 Generated Content:")
                        st.write(content)
                        log_command(f"AI Task: Generated {content_type} about {topic} using {ai_model}")
                        
                    except Exception as e:
                        st.error(f"Error generating content: {e}")
    
    elif task_category == "💻 Code Generation":
        st.subheader("💻 AI Code Generator")
        
        programming_language = st.selectbox("Programming Language:", [
            "Python", "JavaScript", "Java", "C++", "SQL", "HTML/CSS", "React", "Node.js"
        ])
        
        code_task = st.text_area(
            "Describe what you want the code to do:",
            placeholder="Create a function that...\nBuild a web app that...\nWrite a script that..."
        )
        
        if st.button("💻 Generate Code"):
            if code_task:
                with st.spinner("🤖 Generating code..."):
                    try:
                        prompt = f"""Write {programming_language} code for the following task:

Task: {code_task}

Please provide:
1. Clean, well-commented code
2. Explanation of how the code works
3. Usage examples
4. Any dependencies or requirements

Make sure the code is production-ready and follows best practices."""
                        
                        if "OpenAI" in ai_model:
                            if not st.session_state.get('openai_api_key'):
                                st.error("Please provide OpenAI API key")
                                return
                            
                            response = openai.ChatCompletion.create(
                                model="gpt-4" if "GPT-4" in ai_model else "gpt-3.5-turbo",
                                messages=[{"role": "user", "content": prompt}],
                                max_tokens=1000,
                                temperature=0.3
                            )
                            code = response.choices[0].message.content
                        
                        elif "Gemini" in ai_model:
                            if not st.session_state.get('gemini_api_key'):
                                st.error("Please provide Gemini API key")
                                return
                            
                            model = genai.GenerativeModel("gemini-pro")
                            response = model.generate_content(prompt)
                            code = response.text
                        
                        else:
                            code = "Model not configured properly."
                        
                        st.success("💻 Generated Code:")
                        st.code(code, language=programming_language.lower())
                        log_command(f"AI Task: Generated {programming_language} code using {ai_model}")
                        
                    except Exception as e:
                        st.error(f"Error generating code: {e}")
    
    else:
        st.info(f"{task_category} features coming soon! 🚧")

# Legacy chatbot options (keeping for backward compatibility)
def legacy_chatbot_section():
    st.subheader("🤖 Legacy Chatbot Options")
    
    chatbot_option = st.selectbox("Select Chatbot Version", [
        "Chatbot 1 - Gemini Finance Bot",
        "Chatbot 2 - FAQ Bot",
        "Chatbot 3 - Sentiment-Aware",
        "Chatbot 4 - Generative AI"
    ])

    if chatbot_option == "Chatbot 1 - Gemini Finance Bot":
        st.markdown("### Ask me anything about **Stock Market & Finance**")
        
        if st.session_state.get('gemini_api_key'):
            genai.configure(api_key=st.session_state.gemini_api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

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
        else:
            st.warning("Please provide Gemini API key in the configuration section.")

    elif chatbot_option == "Chatbot 2 - FAQ Bot":
        st.write("Chatbot 2: Answering FAQs... (Coming soon)")

    elif chatbot_option == "Chatbot 3 - Sentiment-Aware":
        st.write("Chatbot 3: Detecting your emotion and responding accordingly... (Coming soon)")

    elif chatbot_option == "Chatbot 4 - Generative AI":
        st.write("Chatbot 4: Generating AI-based dynamic response... (Coming soon)")

    else:
        st.error("Invalid chatbot selected.")
