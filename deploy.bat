@echo off
chcp 65001 >nul
title Universal Automation Platform Deployment Script

echo 🚀 Universal Automation Platform Deployment Script
echo ==================================================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in a git repository
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo ❌ Not in a git repository. Please initialize git first.
    echo Run: git init ^&^& git add . ^&^& git commit -m "Initial commit"
    pause
    exit /b 1
)

:menu
cls
echo.
echo Choose deployment option:
echo 1) 🎯 Deploy to Streamlit Cloud (Recommended)
echo 2) 🌐 Deploy to Netlify (Static)
echo 3) 🐳 Build Docker Image
echo 4) 🧪 Test Locally
echo 5) 🔍 Check Dependencies
echo 6) 📋 Show Deployment Guide
echo 7) ❌ Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto streamlit
if "%choice%"=="2" goto netlify
if "%choice%"=="3" goto docker
if "%choice%"=="4" goto local
if "%choice%"=="5" goto check
if "%choice%"=="6" goto guide
if "%choice%"=="7" goto exit
echo ❌ Invalid choice. Please enter 1-7.
pause
goto menu

:streamlit
echo.
echo 📦 Deploying to Streamlit Cloud...
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Ready for Streamlit Cloud deployment"
echo    git push origin main
echo.
echo 2. Go to https://streamlit.io/cloud
echo 3. Sign up/Login with GitHub
echo 4. Click "New app"
echo 5. Select your repository
echo 6. Set main file path: app.py
echo 7. Click "Deploy"
echo.
echo ✅ Your app will be live at: https://your-app-name.streamlit.app
pause
goto menu

:netlify
echo.
echo 🌐 Deploying to Netlify (Static Version)...
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Ready for Netlify deployment"
echo    git push origin main
echo.
echo 2. Go to https://netlify.com
echo 3. Sign up/Login with GitHub
echo 4. Click "New site from Git"
echo 5. Select your repository
echo 6. Build settings:
echo    - Build command: (leave empty)
echo    - Publish directory: .
echo 7. Click "Deploy site"
echo.
echo ⚠️  Note: This creates a static version with limited functionality
pause
goto menu

:docker
echo.
echo 🐳 Building Docker image...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker first.
    pause
    goto menu
)

docker build -t universal-automation-platform .
if errorlevel 1 (
    echo ❌ Docker build failed
) else (
    echo ✅ Docker image built successfully!
    echo Run with: docker run -p 8501:8501 universal-automation-platform
)
pause
goto menu

:check
echo.
echo 🔍 Checking dependencies...

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    pause
    goto menu
)

if not exist "app.py" (
    echo ❌ app.py not found
    pause
    goto menu
)

echo ✅ All required files found
pause
goto menu

:local
echo.
echo 🧪 Testing locally...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    pause
    goto menu
)

pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed
    pause
    goto menu
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Streamlit app...
echo Your app will be available at: http://localhost:8501
echo Press Ctrl+C to stop
echo.

streamlit run app.py
pause
goto menu

:guide
echo.
echo 📋 Deployment Guide:
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
echo Quick Start:
echo 1. Push code to GitHub
echo 2. Choose deployment platform
echo 3. Follow platform-specific instructions
echo.
pause
goto menu

:exit
echo �� Goodbye!
exit /b 0 