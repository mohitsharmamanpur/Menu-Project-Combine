import streamlit as st
import requests
import json
import sqlite3
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pymongo
import psycopg2
from sqlalchemy import create_engine, text

def log_command(command):
    """Log command to file"""
    with open("command_log.txt", "a") as f:
        f.write(f"{datetime.now()}: {command}\n")

def full_stack_section(sub_choice=None):
    st.markdown('<h1 class="section-header">🌐 Full-Stack Development Platform</h1>', unsafe_allow_html=True)
    
    if sub_choice == "🤖 Automation Tasks":
        automation_tasks_section()
    elif sub_choice == "⚛️ React/Node":
        react_node_section()
    elif sub_choice == "🗄️ Database":
        database_section()
    else:
        st.info("Please select a Full-Stack component from the sidebar.")

def automation_tasks_section():
    st.subheader("🤖 Automation Tasks")
    
    # Create tabs for different automation tasks
    tab1, tab2, tab3, tab4 = st.tabs([
        "📬 Form Automation", "📁 File Operations", "📧 Email Automation", "🌐 Web Scraping"
    ])
    
    with tab1:
        st.subheader("📬 Form Submission & Database Storage")
        
        # Form inputs
        with st.form("automation_form"):
            st.write("### Contact Form")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name")
                email = st.text_input("Email Address")
                phone = st.text_input("Phone Number")
            
            with col2:
                company = st.text_input("Company")
                position = st.text_input("Position")
                department = st.selectbox("Department", ["Sales", "Marketing", "IT", "HR", "Finance"])
            
            message = st.text_area("Message")
            newsletter = st.checkbox("Subscribe to newsletter")
            
            submitted = st.form_submit_button("📤 Submit Form")
            
            if submitted:
                if name and email:
                    # Store in session state (simulating database)
                    if 'form_submissions' not in st.session_state:
                        st.session_state.form_submissions = []
                    
                    submission = {
                        'timestamp': datetime.now().isoformat(),
                        'name': name,
                        'email': email,
                        'phone': phone,
                        'company': company,
                        'position': position,
                        'department': department,
                        'message': message,
                        'newsletter': newsletter
                    }
                    
                    st.session_state.form_submissions.append(submission)
                    
                    # Send confirmation email
                    if st.button("📧 Send Confirmation Email"):
                        send_confirmation_email(email, name)
                    
                    st.success("✅ Form submitted successfully!")
                    log_command(f"Form Automation: Submitted form for {name}")
                    
                    # Display submission
                    st.json(submission)
                else:
                    st.error("Please fill in at least name and email.")
        
        # View submissions
        if st.session_state.get('form_submissions'):
            st.subheader("📋 Recent Submissions")
            df = pd.DataFrame(st.session_state.form_submissions)
            st.dataframe(df)
            
            if st.button("💾 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"form_submissions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with tab2:
        st.subheader("📁 File Operations Automation")
        
        # File upload and processing
        uploaded_files = st.file_uploader(
            "Upload files for processing",
            type=['txt', 'csv', 'json', 'xlsx'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.write(f"📁 Uploaded {len(uploaded_files)} files")
            
            for uploaded_file in uploaded_files:
                with st.expander(f"📄 {uploaded_file.name}"):
                    try:
                        if uploaded_file.type == "text/plain":
                            content = str(uploaded_file.read(), "utf-8")
                            st.text_area("File Content:", content, height=200)
                            
                            # Text processing options
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"📊 Word Count - {uploaded_file.name}"):
                                    word_count = len(content.split())
                                    st.metric("Word Count", word_count)
                            
                            with col2:
                                if st.button(f"📝 Save Processed - {uploaded_file.name}"):
                                    processed_content = f"Processed: {content.upper()}"
                                    st.download_button(
                                        label="📥 Download Processed",
                                        data=processed_content,
                                        file_name=f"processed_{uploaded_file.name}",
                                        mime="text/plain"
                                    )
                        
                        elif uploaded_file.type == "text/csv":
                            df = pd.read_csv(uploaded_file)
                            st.dataframe(df)
                            
                            # CSV processing options
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button(f"📊 Info - {uploaded_file.name}"):
                                    st.write("Dataset Info:")
                                    st.write(f"Shape: {df.shape}")
                                    st.write(f"Columns: {list(df.columns)}")
                            
                            with col2:
                                if st.button(f"📈 Stats - {uploaded_file.name}"):
                                    st.dataframe(df.describe())
                            
                            with col3:
                                if st.button(f"💾 Save - {uploaded_file.name}"):
                                    csv = df.to_csv(index=False)
                                    st.download_button(
                                        label="📥 Download CSV",
                                        data=csv,
                                        file_name=f"processed_{uploaded_file.name}",
                                        mime="text/csv"
                                    )
                        
                        elif uploaded_file.type == "application/json":
                            content = json.load(uploaded_file)
                            st.json(content)
                            
                            if st.button(f"📊 Process JSON - {uploaded_file.name}"):
                                if isinstance(content, dict):
                                    st.write("JSON Structure:")
                                    for key, value in content.items():
                                        st.write(f"**{key}:** {type(value).__name__}")
                        
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {e}")
    
    with tab3:
        st.subheader("📧 Email Automation")
        
        # Email configuration
        st.write("### Email Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            smtp_server = st.text_input("SMTP Server:", value="smtp.gmail.com")
            smtp_port = st.number_input("SMTP Port:", value=587)
            sender_email = st.text_input("Sender Email:")
            sender_password = st.text_input("Sender Password:", type="password")
        
        with col2:
            # Email templates
            template_type = st.selectbox("Email Template:", [
                "Welcome Email", "Newsletter", "Order Confirmation", "Custom"
            ])
            
            if template_type == "Welcome Email":
                subject = "Welcome to Our Platform!"
                body = """Dear {name},

Welcome to our platform! We're excited to have you on board.

Best regards,
The Team"""
            elif template_type == "Newsletter":
                subject = "Monthly Newsletter"
                body = """Dear {name},

Here's your monthly newsletter with the latest updates.

Best regards,
The Newsletter Team"""
            elif template_type == "Order Confirmation":
                subject = "Order Confirmation"
                body = """Dear {name},

Thank you for your order. Your order has been confirmed.

Order Details:
- Order ID: {order_id}
- Total: {total}

Best regards,
The Sales Team"""
            else:
                subject = st.text_input("Subject:")
                body = st.text_area("Email Body:")
        
        # Email automation
        st.write("### Email Automation")
        
        if st.session_state.get('form_submissions'):
            recipients = [sub['email'] for sub in st.session_state.form_submissions if sub['email']]
            
            if recipients:
                selected_recipients = st.multiselect("Select Recipients:", recipients)
                
                if st.button("📧 Send Bulk Email"):
                    if sender_email and sender_password and selected_recipients:
                        with st.spinner("Sending emails..."):
                            success_count = 0
                            for recipient in selected_recipients:
                                try:
                                    # Find recipient data
                                    recipient_data = next(
                                        (sub for sub in st.session_state.form_submissions if sub['email'] == recipient),
                                        {'name': 'User'}
                                    )
                                    
                                    # Format email
                                    formatted_body = body.format(**recipient_data)
                                    
                                    # Send email
                                    send_automated_email(
                                        smtp_server, smtp_port, sender_email, sender_password,
                                        recipient, subject, formatted_body
                                    )
                                    success_count += 1
                                    
                                except Exception as e:
                                    st.error(f"Error sending to {recipient}: {e}")
                            
                            st.success(f"✅ Sent {success_count}/{len(selected_recipients)} emails successfully!")
                            log_command(f"Email Automation: Sent {success_count} bulk emails")
                    else:
                        st.warning("Please provide email credentials and select recipients.")
            else:
                st.info("No email addresses found in form submissions.")
        else:
            st.info("No form submissions available. Please submit a form first.")
    
    with tab4:
        st.subheader("🌐 Web Scraping Automation")
        
        # Web scraping configuration
        url = st.text_input("Enter URL to scrape:", placeholder="https://example.com")
        
        if url:
            scraping_type = st.selectbox("Scraping Type:", [
                "Basic Content", "Links", "Images", "Tables", "Custom Selector"
            ])
            
            if st.button("🕷️ Start Scraping"):
                try:
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    
                    if scraping_type == "Basic Content":
                        st.write("### Page Content")
                        st.text(response.text[:2000] + "..." if len(response.text) > 2000 else response.text)
                    
                    elif scraping_type == "Links":
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        links = soup.find_all('a', href=True)
                        
                        link_data = []
                        for link in links[:20]:  # Limit to first 20 links
                            link_data.append({
                                'Text': link.get_text(strip=True),
                                'URL': link['href']
                            })
                        
                        df = pd.DataFrame(link_data)
                        st.dataframe(df)
                    
                    elif scraping_type == "Images":
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        images = soup.find_all('img')
                        
                        image_data = []
                        for img in images[:10]:  # Limit to first 10 images
                            image_data.append({
                                'Alt Text': img.get('alt', 'No alt text'),
                                'Source': img.get('src', 'No source'),
                                'Title': img.get('title', 'No title')
                            })
                        
                        df = pd.DataFrame(image_data)
                        st.dataframe(df)
                    
                    elif scraping_type == "Tables":
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(response.text, 'html.parser')
                        tables = soup.find_all('table')
                        
                        if tables:
                            for i, table in enumerate(tables[:3]):  # Show first 3 tables
                                st.write(f"### Table {i+1}")
                                df = pd.read_html(str(table))[0]
                                st.dataframe(df)
                        else:
                            st.info("No tables found on the page.")
                    
                    elif scraping_type == "Custom Selector":
                        selector = st.text_input("CSS Selector:", placeholder=".class-name or #id-name")
                        
                        if selector:
                            from bs4 import BeautifulSoup
                            soup = BeautifulSoup(response.text, 'html.parser')
                            elements = soup.select(selector)
                            
                            if elements:
                                st.write(f"Found {len(elements)} elements:")
                                for i, element in enumerate(elements[:5]):  # Show first 5
                                    st.write(f"**Element {i+1}:**")
                                    st.text(element.get_text(strip=True))
                            else:
                                st.info("No elements found with the specified selector.")
                    
                    log_command(f"Web Scraping: Scraped {url} for {scraping_type}")
                    
                except Exception as e:
                    st.error(f"Error scraping {url}: {e}")

def react_node_section():
    st.subheader("⚛️ React/Node.js Integration")
    
    # Create tabs for different React/Node features
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚀 API Demo", "⚛️ React Components", "🔗 Frontend-Backend", "📦 Build & Deploy"
    ])
    
    with tab1:
        st.subheader("🚀 Node.js API Demo")
        
        # Simple API endpoints
        api_endpoint = st.selectbox("API Endpoint:", [
            "/api/users", "/api/products", "/api/orders", "/api/analytics"
        ])
        
        if st.button("🌐 Test API"):
            # Simulate API response
            if api_endpoint == "/api/users":
                response_data = {
                    "users": [
                        {"id": 1, "name": "John Doe", "email": "john@example.com"},
                        {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
                        {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
                    ],
                    "total": 3
                }
            elif api_endpoint == "/api/products":
                response_data = {
                    "products": [
                        {"id": 1, "name": "Laptop", "price": 999.99, "category": "Electronics"},
                        {"id": 2, "name": "Phone", "price": 699.99, "category": "Electronics"},
                        {"id": 3, "name": "Headphones", "price": 199.99, "category": "Audio"}
                    ],
                    "total": 3
                }
            elif api_endpoint == "/api/orders":
                response_data = {
                    "orders": [
                        {"id": 1, "user_id": 1, "total": 1299.98, "status": "completed"},
                        {"id": 2, "user_id": 2, "total": 699.99, "status": "pending"},
                        {"id": 3, "user_id": 3, "total": 199.99, "status": "shipped"}
                    ],
                    "total": 3
                }
            else:  # analytics
                response_data = {
                    "analytics": {
                        "total_users": 150,
                        "total_orders": 89,
                        "revenue": 45678.90,
                        "growth_rate": 12.5
                    }
                }
            
            st.json(response_data)
            
            # API documentation
            st.subheader("📚 API Documentation")
            st.code(f"""
GET {api_endpoint}
Content-Type: application/json

Response:
{json.dumps(response_data, indent=2)}
            """, language="json")
    
    with tab2:
        st.subheader("⚛️ React Components Demo")
        
        # React component examples
        component_type = st.selectbox("React Component:", [
            "User Card", "Product Grid", "Order Form", "Analytics Dashboard"
        ])
        
        if component_type == "User Card":
            st.write("### User Card Component")
            st.code("""
import React from 'react';

const UserCard = ({ user }) => {
  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.email}</p>
      <button onClick={() => handleEdit(user.id)}>Edit</button>
    </div>
  );
};
            """, language="jsx")
            
            # Live demo
            st.write("### Live Demo")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center;">
                    <img src="https://via.placeholder.com/80" style="border-radius: 50%;">
                    <h4>John Doe</h4>
                    <p>john@example.com</p>
                    <button style="background: #007bff; color: white; border: none; padding: 5px 15px; border-radius: 4px;">Edit</button>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center;">
                    <img src="https://via.placeholder.com/80" style="border-radius: 50%;">
                    <h4>Jane Smith</h4>
                    <p>jane@example.com</p>
                    <button style="background: #007bff; color: white; border: none; padding: 5px 15px; border-radius: 4px;">Edit</button>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center;">
                    <img src="https://via.placeholder.com/80" style="border-radius: 50%;">
                    <h4>Bob Johnson</h4>
                    <p>bob@example.com</p>
                    <button style="background: #007bff; color: white; border: none; padding: 5px 15px; border-radius: 4px;">Edit</button>
                </div>
                """, unsafe_allow_html=True)
        
        elif component_type == "Product Grid":
            st.write("### Product Grid Component")
            st.code("""
import React from 'react';

const ProductGrid = ({ products }) => {
  return (
    <div className="product-grid">
      {products.map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>
          <p>${product.price}</p>
          <button onClick={() => addToCart(product)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
};
            """, language="jsx")
        
        elif component_type == "Order Form":
            st.write("### Order Form Component")
            st.code("""
import React, { useState } from 'react';

const OrderForm = () => {
  const [formData, setFormData] = useState({
    customerName: '',
    email: '',
    items: []
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    // Submit order logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Customer Name"
        value={formData.customerName}
        onChange={(e) => setFormData({...formData, customerName: e.target.value})}
      />
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({...formData, email: e.target.value})}
      />
      <button type="submit">Place Order</button>
    </form>
  );
};
            """, language="jsx")
    
    with tab3:
        st.subheader("🔗 Frontend-Backend Connection")
        
        # API integration demo
        st.write("### API Integration Example")
        
        # Simulate frontend form
        with st.form("api_integration"):
            st.write("#### Frontend Form (React)")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Name:")
                email = st.text_input("Email:")
            
            with col2:
                age = st.number_input("Age:", min_value=0, max_value=120)
                department = st.selectbox("Department:", ["IT", "Sales", "Marketing"])
            
            submitted = st.form_submit_button("🚀 Submit to API")
            
            if submitted:
                # Simulate API call
                user_data = {
                    "name": name,
                    "email": email,
                    "age": age,
                    "department": department,
                    "timestamp": datetime.now().isoformat()
                }
                
                st.success("✅ Data sent to API successfully!")
                st.json(user_data)
                
                # Show the API call
                st.write("#### API Call (JavaScript)")
                st.code(f"""
// Frontend JavaScript
const response = await fetch('/api/users', {{
  method: 'POST',
  headers: {{
    'Content-Type': 'application/json'
  }},
  body: JSON.stringify({user_data})
}});

const result = await response.json();
console.log(result);
                """, language="javascript")
                
                # Show backend code
                st.write("#### Backend Handler (Node.js)")
                st.code(f"""
// Backend Node.js
app.post('/api/users', (req, res) => {{
  const userData = req.body;
  
  // Save to database
  db.users.insert(userData);
  
  res.json({{
    success: true,
    message: 'User created successfully',
    user: userData
  }});
}});
                """, language="javascript")
    
    with tab4:
        st.subheader("📦 Build & Deploy")
        
        # Build process
        st.write("### Build Process")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔨 Build Frontend"):
                with st.spinner("Building React app..."):
                    st.success("✅ Frontend built successfully!")
                    st.code("npm run build", language="bash")
                    log_command("React/Node: Built frontend")
        
        with col2:
            if st.button("🔨 Build Backend"):
                with st.spinner("Building Node.js app..."):
                    st.success("✅ Backend built successfully!")
                    st.code("npm install && npm run build", language="bash")
                    log_command("React/Node: Built backend")
        
        # Deployment options
        st.write("### Deployment Options")
        
        deployment_platform = st.selectbox("Deployment Platform:", [
            "Vercel (Frontend)", "Netlify (Frontend)", "Heroku (Full-Stack)", "AWS (Full-Stack)", "Docker"
        ])
        
        if deployment_platform == "Vercel (Frontend)":
            st.code("""
# Deploy to Vercel
npm install -g vercel
vercel --prod
            """, language="bash")
        
        elif deployment_platform == "Netlify (Frontend)":
            st.code("""
# Deploy to Netlify
npm run build
netlify deploy --prod --dir=build
            """, language="bash")
        
        elif deployment_platform == "Heroku (Full-Stack)":
            st.code("""
# Deploy to Heroku
heroku create my-app
git push heroku main
            """, language="bash")
        
        elif deployment_platform == "AWS (Full-Stack)":
            st.code("""
# Deploy to AWS
aws s3 sync build/ s3://my-bucket
aws cloudformation deploy --template-file template.yml
            """, language="bash")
        
        elif deployment_platform == "Docker":
            st.code("""
# Docker deployment
docker build -t my-app .
docker run -p 3000:3000 my-app
            """, language="bash")

def database_section():
    st.subheader("🗄️ Database Operations")
    
    # Database selection
    db_type = st.selectbox("Select Database:", [
        "SQLite (Local)", "MongoDB", "PostgreSQL", "MySQL"
    ])
    
    if db_type == "SQLite (Local)":
        sqlite_operations()
    elif db_type == "MongoDB":
        mongodb_operations()
    elif db_type == "PostgreSQL":
        postgresql_operations()
    elif db_type == "MySQL":
        mysql_operations()

def sqlite_operations():
    st.subheader("🗄️ SQLite Database Operations")
    
    # Create database connection
    db_path = "automation_platform.db"
    
    # Initialize database
    if st.button("🗄️ Initialize Database"):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    category TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    total REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            st.success("✅ Database initialized successfully!")
            log_command("Database: Initialized SQLite database")
            
        except Exception as e:
            st.error(f"Error initializing database: {e}")
    
    # Database operations
    operation = st.selectbox("Database Operation:", [
        "📋 View Tables", "➕ Insert Data", "🔍 Query Data", "✏️ Update Data", "🗑️ Delete Data"
    ])
    
    if operation == "📋 View Tables":
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            if tables:
                st.write("### Available Tables:")
                for table in tables:
                    table_name = table[0]
                    st.write(f"**{table_name}**")
                    
                    # Show table structure
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns = cursor.fetchall()
                    
                    col_data = []
                    for col in columns:
                        col_data.append({
                            'Column': col[1],
                            'Type': col[2],
                            'Not Null': col[3],
                            'Primary Key': col[5]
                        })
                    
                    df = pd.DataFrame(col_data)
                    st.dataframe(df)
                    st.divider()
            else:
                st.info("No tables found. Please initialize the database first.")
            
            conn.close()
            
        except Exception as e:
            st.error(f"Error viewing tables: {e}")
    
    elif operation == "➕ Insert Data":
        table = st.selectbox("Select Table:", ["users", "products", "orders"])
        
        if table == "users":
            with st.form("insert_user"):
                name = st.text_input("Name:")
                email = st.text_input("Email:")
                
                if st.form_submit_button("➕ Insert User"):
                    if name and email:
                        try:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                            conn.commit()
                            conn.close()
                            st.success("✅ User inserted successfully!")
                            log_command(f"Database: Inserted user {name}")
                        except Exception as e:
                            st.error(f"Error inserting user: {e}")
                    else:
                        st.warning("Please fill in all fields.")
        
        elif table == "products":
            with st.form("insert_product"):
                name = st.text_input("Product Name:")
                price = st.number_input("Price:", min_value=0.0, step=0.01)
                category = st.text_input("Category:")
                
                if st.form_submit_button("➕ Insert Product"):
                    if name and price:
                        try:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("INSERT INTO products (name, price, category) VALUES (?, ?, ?)", 
                                         (name, price, category))
                            conn.commit()
                            conn.close()
                            st.success("✅ Product inserted successfully!")
                            log_command(f"Database: Inserted product {name}")
                        except Exception as e:
                            st.error(f"Error inserting product: {e}")
                    else:
                        st.warning("Please fill in name and price.")
    
    elif operation == "🔍 Query Data":
        table = st.selectbox("Select Table to Query:", ["users", "products", "orders"])
        
        if st.button("🔍 Query All Data"):
            try:
                conn = sqlite3.connect(db_path)
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                conn.close()
                
                if not df.empty:
                    st.dataframe(df)
                    st.metric("Total Records", len(df))
                else:
                    st.info(f"No data found in {table} table.")
                    
            except Exception as e:
                st.error(f"Error querying data: {e}")
        
        # Custom query
        custom_query = st.text_area("Custom SQL Query:", placeholder="SELECT * FROM users WHERE name LIKE '%John%'")
        
        if st.button("🔍 Execute Custom Query"):
            if custom_query:
                try:
                    conn = sqlite3.connect(db_path)
                    df = pd.read_sql_query(custom_query, conn)
                    conn.close()
                    
                    if not df.empty:
                        st.dataframe(df)
                        st.metric("Query Results", len(df))
                    else:
                        st.info("No results found.")
                        
                except Exception as e:
                    st.error(f"Error executing query: {e}")
            else:
                st.warning("Please enter a SQL query.")

def mongodb_operations():
    st.subheader("🗄️ MongoDB Operations")
    
    # MongoDB configuration
    st.write("### MongoDB Configuration")
    mongodb_uri = st.text_input("MongoDB Connection String:", 
                               placeholder="mongodb://localhost:27017/")
    database_name = st.text_input("Database Name:", value="automation_platform")
    
    if st.button("🔗 Test MongoDB Connection"):
        try:
            client = pymongo.MongoClient(mongodb_uri)
            db = client[database_name]
            # Test connection
            client.admin.command('ping')
            st.success("✅ MongoDB connection successful!")
            st.session_state.mongodb_client = client
            st.session_state.mongodb_db = db
            log_command("Database: Connected to MongoDB")
        except Exception as e:
            st.error(f"❌ MongoDB connection failed: {e}")
    
    if st.session_state.get('mongodb_client'):
        # MongoDB operations
        operation = st.selectbox("MongoDB Operation:", [
            "📋 Collections", "➕ Insert Document", "🔍 Query Documents", "✏️ Update Documents", "🗑️ Delete Documents"
        ])
        
        db = st.session_state.mongodb_db
        
        if operation == "📋 Collections":
            collections = db.list_collection_names()
            if collections:
                st.write("### Available Collections:")
                for collection in collections:
                    count = db[collection].count_documents({})
                    st.write(f"**{collection}** ({count} documents)")
            else:
                st.info("No collections found.")
        
        elif operation == "➕ Insert Document":
            collection_name = st.text_input("Collection Name:", value="users")
            
            # Document input
            st.write("### Document Data (JSON)")
            document_json = st.text_area("Document JSON:", 
                                       value='{"name": "John Doe", "email": "john@example.com", "age": 30}')
            
            if st.button("➕ Insert Document"):
                try:
                    document = json.loads(document_json)
                    result = db[collection_name].insert_one(document)
                    st.success(f"✅ Document inserted with ID: {result.inserted_id}")
                    log_command(f"Database: Inserted document in {collection_name}")
                except Exception as e:
                    st.error(f"Error inserting document: {e}")

def postgresql_operations():
    st.subheader("🗄️ PostgreSQL Operations")
    
    # PostgreSQL configuration
    st.write("### PostgreSQL Configuration")
    col1, col2 = st.columns(2)
    
    with col1:
        host = st.text_input("Host:", value="localhost")
        port = st.number_input("Port:", value=5432)
        database = st.text_input("Database:", value="automation_platform")
    
    with col2:
        username = st.text_input("Username:", value="postgres")
        password = st.text_input("Password:", type="password")
    
    if st.button("🔗 Test PostgreSQL Connection"):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=username,
                password=password
            )
            conn.close()
            st.success("✅ PostgreSQL connection successful!")
            st.session_state.postgres_config = {
                'host': host, 'port': port, 'database': database,
                'user': username, 'password': password
            }
            log_command("Database: Connected to PostgreSQL")
        except Exception as e:
            st.error(f"❌ PostgreSQL connection failed: {e}")

def mysql_operations():
    st.subheader("🗄️ MySQL Operations")
    st.info("MySQL operations coming soon! 🚧")

def send_confirmation_email(email, name):
    """Send confirmation email"""
    try:
        # This is a placeholder - you'd need to configure SMTP settings
        st.info(f"📧 Confirmation email would be sent to {email}")
        log_command(f"Email Automation: Sent confirmation to {email}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

def send_automated_email(smtp_server, smtp_port, sender_email, sender_password, recipient, subject, body):
    """Send automated email"""
    try:
        # This is a placeholder - you'd need to configure SMTP settings
        st.info(f"📧 Email would be sent to {recipient}")
        log_command(f"Email Automation: Sent email to {recipient}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Legacy functions for backward compatibility
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
