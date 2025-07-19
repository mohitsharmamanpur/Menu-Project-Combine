#!/bin/bash

# Universal Automation Platform Deployment Script
# This script helps deploy the application to various platforms

echo "🚀 Universal Automation Platform Deployment Script"
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please initialize git first."
    echo "Run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Function to deploy to Streamlit Cloud
deploy_streamlit() {
    echo "📦 Deploying to Streamlit Cloud..."
    echo "1. Push your code to GitHub:"
    echo "   git add ."
    echo "   git commit -m 'Ready for Streamlit Cloud deployment'"
    echo "   git push origin main"
    echo ""
    echo "2. Go to https://streamlit.io/cloud"
    echo "3. Sign up/Login with GitHub"
    echo "4. Click 'New app'"
    echo "5. Select your repository"
    echo "6. Set main file path: app.py"
    echo "7. Click 'Deploy'"
    echo ""
    echo "✅ Your app will be live at: https://your-app-name.streamlit.app"
}

# Function to deploy to Netlify
deploy_netlify() {
    echo "🌐 Deploying to Netlify (Static Version)..."
    echo "1. Push your code to GitHub:"
    echo "   git add ."
    echo "   git commit -m 'Ready for Netlify deployment'"
    echo "   git push origin main"
    echo ""
    echo "2. Go to https://netlify.com"
    echo "3. Sign up/Login with GitHub"
    echo "4. Click 'New site from Git'"
    echo "5. Select your repository"
    echo "6. Build settings:"
    echo "   - Build command: (leave empty)"
    echo "   - Publish directory: ."
    echo "7. Click 'Deploy site'"
    echo ""
    echo "⚠️  Note: This creates a static version with limited functionality"
}

# Function to build Docker image
build_docker() {
    echo "🐳 Building Docker image..."
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed. Please install Docker first."
        return 1
    fi
    
    docker build -t universal-automation-platform .
    echo "✅ Docker image built successfully!"
    echo "Run with: docker run -p 8501:8501 universal-automation-platform"
}

# Function to check dependencies
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        echo "❌ requirements.txt not found"
        return 1
    fi
    
    if [ ! -f "app.py" ]; then
        echo "❌ app.py not found"
        return 1
    fi
    
    echo "✅ All required files found"
    return 0
}

# Function to test locally
test_local() {
    echo "🧪 Testing locally..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 is not installed"
        return 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        echo "❌ pip3 is not installed"
        return 1
    fi
    
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    
    echo "Starting Streamlit app..."
    echo "Your app will be available at: http://localhost:8501"
    echo "Press Ctrl+C to stop"
    
    streamlit run app.py
}

# Main menu
while true; do
    echo ""
    echo "Choose deployment option:"
    echo "1) 🎯 Deploy to Streamlit Cloud (Recommended)"
    echo "2) 🌐 Deploy to Netlify (Static)"
    echo "3) 🐳 Build Docker Image"
    echo "4) 🧪 Test Locally"
    echo "5) 🔍 Check Dependencies"
    echo "6) 📋 Show Deployment Guide"
    echo "7) ❌ Exit"
    echo ""
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            deploy_streamlit
            ;;
        2)
            deploy_netlify
            ;;
        3)
            build_docker
            ;;
        4)
            test_local
            ;;
        5)
            check_dependencies
            ;;
        6)
            echo "📋 Opening deployment guide..."
            if command -v cat &> /dev/null; then
                cat DEPLOYMENT_GUIDE.md
            else
                echo "Deployment guide available in DEPLOYMENT_GUIDE.md"
            fi
            ;;
        7)
            echo "👋 Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1-7."
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
done 