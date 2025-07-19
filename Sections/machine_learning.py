import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
import io
import base64

def log_command(command):
    """Log command to file"""
    with open("command_log.txt", "a") as f:
        f.write(f"{pd.Timestamp.now()}: {command}\n")

def create_download_link(df, filename, text):
    """Create a download link for dataframe"""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def plot_confusion_matrix(y_true, y_pred, classes):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    return fig

def machine_learning_section():
    st.markdown('<h1 class="section-header">🧠 Machine Learning Platform</h1>', unsafe_allow_html=True)
    
    # Create tabs for different ML tasks
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📁 Data Upload & Analysis", 
        "🔧 Data Preprocessing", 
        "🤖 Model Training", 
        "🎯 Predictions", 
        "📊 Model Evaluation"
    ])
    
    with tab1:
        st.subheader("📁 Upload Your Dataset")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV file", 
            type=['csv'],
            help="Upload your dataset in CSV format"
        )
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ Dataset loaded successfully! Shape: {df.shape}")
                
                # Display basic info
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📋 Dataset Info")
                    buffer = io.StringIO()
                    df.info(buf=buffer)
                    st.text(buffer.getvalue())
                
                with col2:
                    st.subheader("📊 Basic Statistics")
                    st.dataframe(df.describe())
                
                # Display first few rows
                st.subheader("👀 First 10 Rows")
                st.dataframe(df.head(10))
                
                # Data visualization
                st.subheader("📈 Data Visualization")
                
                # Select columns for visualization
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                
                if numeric_cols:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Histogram
                        selected_col = st.selectbox("Select column for histogram:", numeric_cols)
                        fig = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Box plot
                        fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
                        st.plotly_chart(fig, use_container_width=True)
                
                # Correlation matrix for numeric columns
                if len(numeric_cols) > 1:
                    st.subheader("🔗 Correlation Matrix")
                    corr_matrix = df[numeric_cols].corr()
                    fig = px.imshow(corr_matrix, 
                                  title="Correlation Matrix",
                                  color_continuous_scale='RdBu')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Store dataframe in session state
                st.session_state.df = df
                st.session_state.numeric_cols = numeric_cols
                st.session_state.categorical_cols = categorical_cols
                
                log_command(f"Uploaded dataset: {uploaded_file.name} with shape {df.shape}")
                
            except Exception as e:
                st.error(f"Error loading file: {e}")
    
    with tab2:
        st.subheader("🔧 Data Preprocessing")
        
        if 'df' not in st.session_state:
            st.warning("Please upload a dataset first in the 'Data Upload & Analysis' tab.")
        else:
            df = st.session_state.df.copy()
            
            # Handle missing values
            st.subheader("🧹 Missing Values")
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                st.write("Missing values found:")
                st.dataframe(missing_data[missing_data > 0])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Remove rows with missing values"):
                        df = df.dropna()
                        st.success(f"Removed missing values. New shape: {df.shape}")
                
                with col2:
                    if st.button("Fill missing values with mean (numeric)"):
                        numeric_cols = df.select_dtypes(include=[np.number]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.success("Filled missing numeric values with mean")
            else:
                st.success("✅ No missing values found!")
            
            # Handle categorical variables
            if st.session_state.categorical_cols:
                st.subheader("🏷️ Categorical Variables")
                for col in st.session_state.categorical_cols:
                    if st.checkbox(f"Encode {col}"):
                        le = LabelEncoder()
                        df[col] = le.fit_transform(df[col])
                        st.success(f"Encoded {col}")
            
            # Feature scaling
            st.subheader("⚖️ Feature Scaling")
            if st.checkbox("Apply Standard Scaling to numeric features"):
                scaler = StandardScaler()
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
                st.success("Applied Standard Scaling")
            
            # Update session state
            st.session_state.df_processed = df
            st.subheader("✅ Preprocessed Data Preview")
            st.dataframe(df.head())
            
            # Download processed data
            if st.button("💾 Download Processed Data"):
                st.markdown(create_download_link(df, "processed_data.csv", "Download Processed CSV"), unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🤖 Model Training")
        
        if 'df_processed' not in st.session_state:
            st.warning("Please preprocess your data first in the 'Data Preprocessing' tab.")
        else:
            df = st.session_state.df_processed
            
            # Model selection
            model_type = st.selectbox(
                "Select Model Type",
                ["Linear Regression", "Logistic Regression", "Random Forest", "Support Vector Machine"]
            )
            
            # Target variable selection
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            target_col = st.selectbox("Select Target Variable:", numeric_cols)
            
            # Feature selection
            feature_cols = [col for col in numeric_cols if col != target_col]
            selected_features = st.multiselect("Select Features:", feature_cols, default=feature_cols)
            
            if selected_features and target_col:
                X = df[selected_features]
                y = df[target_col]
                
                # Split data
                test_size = st.slider("Test Size:", 0.1, 0.5, 0.2, 0.05)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                
                # Train model
                if st.button("🚀 Train Model"):
                    with st.spinner("Training model..."):
                        if model_type == "Linear Regression":
                            model = LinearRegression()
                        elif model_type == "Logistic Regression":
                            model = LogisticRegression()
                        elif model_type == "Random Forest":
                            if len(y.unique()) > 10:  # Regression
                                model = RandomForestRegressor(n_estimators=100, random_state=42)
                            else:  # Classification
                                model = RandomForestClassifier(n_estimators=100, random_state=42)
                        elif model_type == "Support Vector Machine":
                            if len(y.unique()) > 10:  # Regression
                                model = SVR()
                            else:  # Classification
                                model = SVC()
                        
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        
                        # Store model and results
                        st.session_state.model = model
                        st.session_state.X_test = X_test
                        st.session_state.y_test = y_test
                        st.session_state.y_pred = y_pred
                        st.session_state.model_type = model_type
                        
                        st.success(f"✅ {model_type} trained successfully!")
                        
                        # Cross-validation
                        cv_scores = cross_val_score(model, X, y, cv=5)
                        st.metric("Cross-validation Score", f"{cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
                        
                        log_command(f"Trained {model_type} model on {len(selected_features)} features")
    
    with tab4:
        st.subheader("🎯 Make Predictions")
        
        if 'model' not in st.session_state:
            st.warning("Please train a model first in the 'Model Training' tab.")
        else:
            model = st.session_state.model
            model_type = st.session_state.model_type
            
            # Single prediction
            st.subheader("📝 Single Prediction")
            
            if 'df_processed' in st.session_state:
                df = st.session_state.df_processed
                feature_cols = [col for col in df.select_dtypes(include=[np.number]).columns 
                              if col != st.session_state.get('target_col', '')]
                
                # Create input form
                input_data = {}
                col1, col2 = st.columns(2)
                
                for i, col in enumerate(feature_cols):
                    if i % 2 == 0:
                        with col1:
                            input_data[col] = st.number_input(f"Enter {col}:", value=float(df[col].mean()))
                    else:
                        with col2:
                            input_data[col] = st.number_input(f"Enter {col}:", value=float(df[col].mean()))
                
                if st.button("🔮 Predict"):
                    input_df = pd.DataFrame([input_data])
                    prediction = model.predict(input_df)[0]
                    
                    if model_type in ["Linear Regression", "Random Forest"] and len(st.session_state.y_test.unique()) > 10:
                        st.success(f"Predicted Value: {prediction:.2f}")
                    else:
                        st.success(f"Predicted Class: {prediction}")
            
            # Batch prediction
            st.subheader("📊 Batch Prediction")
            uploaded_pred_file = st.file_uploader("Upload CSV for batch prediction", type=['csv'])
            
            if uploaded_pred_file is not None:
                try:
                    pred_df = pd.read_csv(uploaded_pred_file)
                    st.write("Preview of prediction data:")
                    st.dataframe(pred_df.head())
                    
                    if st.button("🔮 Predict Batch"):
                        predictions = model.predict(pred_df)
                        pred_df['Prediction'] = predictions
                        st.success("Batch prediction completed!")
                        st.dataframe(pred_df)
                        
                        # Download predictions
                        st.markdown(create_download_link(pred_df, "predictions.csv", "Download Predictions"), unsafe_allow_html=True)
                        
                        log_command(f"Made batch predictions on {len(pred_df)} samples")
                
                except Exception as e:
                    st.error(f"Error in batch prediction: {e}")
    
    with tab5:
        st.subheader("📊 Model Evaluation")
        
        if 'model' not in st.session_state:
            st.warning("Please train a model first in the 'Model Training' tab.")
        else:
            model = st.session_state.model
            y_test = st.session_state.y_test
            y_pred = st.session_state.y_pred
            model_type = st.session_state.model_type
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if model_type in ["Linear Regression", "Random Forest"] and len(y_test.unique()) > 10:
                    mse = mean_squared_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    st.metric("Mean Squared Error", f"{mse:.4f}")
                    st.metric("R² Score", f"{r2:.4f}")
                else:
                    accuracy = accuracy_score(y_test, y_pred)
                    st.metric("Accuracy", f"{accuracy:.4f}")
            
            with col2:
                st.subheader("📈 Actual vs Predicted")
                fig = px.scatter(x=y_test, y=y_pred, 
                               title="Actual vs Predicted Values",
                               labels={'x': 'Actual', 'y': 'Predicted'})
                fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], 
                                       y=[y_test.min(), y_test.max()], 
                                       mode='lines', name='Perfect Prediction'))
                st.plotly_chart(fig, use_container_width=True)
            
            with col3:
                if model_type not in ["Linear Regression"] and len(y_test.unique()) <= 10:
                    st.subheader("📊 Confusion Matrix")
                    classes = sorted(y_test.unique())
                    fig = plot_confusion_matrix(y_test, y_pred, classes)
                    st.pyplot(fig)
                    
                    # Classification report
                    st.subheader("📋 Classification Report")
                    report = classification_report(y_test, y_pred, output_dict=True)
                    st.dataframe(pd.DataFrame(report).transpose())
            
            # Feature importance (for tree-based models)
            if hasattr(model, 'feature_importances_'):
                st.subheader("🎯 Feature Importance")
                feature_importance = pd.DataFrame({
                    'feature': st.session_state.df_processed[st.session_state.get('selected_features', [])].columns,
                    'importance': model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                fig = px.bar(feature_importance, x='importance', y='feature', 
                           title="Feature Importance",
                           orientation='h')
                st.plotly_chart(fig, use_container_width=True)
    
    # Quick ML Models (existing functionality)
    st.divider()
    st.subheader("🚀 Quick ML Models")
    
    ml_model = st.selectbox("Select Quick ML Model", [
        "💰 Salary Prediction (Linear Regression)",
        "🏢 Startup Profit Prediction (Multiple Linear Regression)",
        "📊 Customer Segmentation (K-Means)",
        "🎯 Credit Card Fraud Detection (Random Forest)",
        "🏠 House Price Prediction (Random Forest)"
    ])
    
    if ml_model == "💰 Salary Prediction (Linear Regression)":
        try:
            dataset = pd.read_csv("Data/Salary-data.csv")
            x = dataset["YearsExperience"].values.reshape(-1, 1)
            y = dataset["Salary"].values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(x, y)
            
            col1, col2 = st.columns(2)
            with col1:
                years_exp = st.number_input("Enter Years of Experience:", min_value=0.0, max_value=50.0, step=0.1)
                if st.button("Predict Salary"):
                    prediction = model.predict([[years_exp]])
                    st.success(f"Predicted Salary: ₹ {prediction[0][0]:,.2f}")
            
            with col2:
                # Plot the data
                fig = px.scatter(dataset, x="YearsExperience", y="Salary", 
                               title="Salary vs Years of Experience")
                fig.add_trace(go.Scatter(x=dataset["YearsExperience"], 
                                       y=model.predict(x).flatten(), 
                                       mode='lines', name='Regression Line'))
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Error: {e}")

    elif ml_model == "🏢 Startup Profit Prediction (Multiple Linear Regression)":
        try:
            dataset = pd.read_csv("Data/50startups.csv")
            dataset = pd.get_dummies(dataset, columns=['State'], drop_first=True)
            x = dataset[['R&D Spend', 'Administration', 'Marketing Spend', 'State_Florida', 'State_New York']]
            y = dataset['Profit']
            model = LinearRegression()
            model.fit(x, y)
            
            st.markdown("### Enter Startup Investment Details")
            col1, col2 = st.columns(2)
            
            with col1:
                rd_spend = st.number_input("R&D Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
                admin = st.number_input("Administration Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
                marketing = st.number_input("Marketing Spend (₹)", min_value=0.0, step=1000.0, format="%.2f")
            
            with col2:
                state = st.selectbox("State", ["California", "Florida", "New York"])
                state_florida = 1 if state == "Florida" else 0
                state_newyork = 1 if state == "New York" else 0
                
                if st.button("Predict Profit"):
                    input_data = [[rd_spend, admin, marketing, state_florida, state_newyork]]
                    prediction = model.predict(input_data)
                    st.success(f"Predicted Profit: ₹ {prediction[0]:,.2f}")
                    
                    # Show feature importance
                    feature_importance = pd.DataFrame({
                        'Feature': ['R&D Spend', 'Administration', 'Marketing Spend', 'State_Florida', 'State_New York'],
                        'Coefficient': model.coef_
                    })
                    st.dataframe(feature_importance)
                    
        except Exception as e:
            st.error(f"Error: {e}")

    else:
        st.info(f"{ml_model} is under construction 🚧. Coming soon!")
