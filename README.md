# 🚀 Universal Automation Platform

A comprehensive automation platform built with Streamlit that combines Machine Learning, DevOps, Cloud Services, AI, and Full-Stack development capabilities.

## 🌟 Features

- **🧠 Machine Learning**: Dataset analysis, model training, and predictions
- **⚙️ DevOps**: Docker, Jenkins, and Kubernetes automation
- **☁️ Cloud Services**: AWS EC2, S3, and EBS management
- **🤖 Agentic AI**: OpenAI/Gemini integration and document Q&A
- **🌐 Full-Stack**: React/Node.js integration and database operations
- **📱 JavaScript**: Camera, location, and social media automation
- **🐧 Linux & 🪟 Windows**: System automation and management
- **🐍 Python**: WhatsApp, email, social media, and web scraping automation

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Fork/Clone** this repository
2. **Sign up** for [Streamlit Cloud](https://streamlit.io/cloud)
3. **Connect** your GitHub repository
4. **Deploy** with one click

**Benefits:**
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ Full Streamlit functionality
- ✅ No configuration needed

### Option 2: Netlify (Static Version)

1. **Push** your code to GitHub
2. **Connect** to Netlify
3. **Deploy** automatically

**Note:** This creates a static version with limited functionality.

### Option 3: Other Platforms

- **Heroku**: `git push heroku main`
- **Railway**: Connect repository and deploy
- **Render**: Connect repository and deploy

## 📋 Prerequisites

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

## 🔧 Configuration Files

- `.streamlit/config.toml` - Streamlit configuration
- `packages.txt` - System dependencies
- `setup.sh` - Deployment setup script
- `netlify.toml` - Netlify configuration
- `requirements.txt` - Python dependencies

## 🛠️ Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd Menu-based-project

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## 📁 Project Structure

```
Menu-based-project/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── Sections/             # Feature modules
│   ├── machine_learning.py
│   ├── Linux.py
│   ├── Windows.py
│   ├── Python.py
│   ├── DevOps.py
│   ├── Cloud.py
│   ├── Agentic_ai.py
│   ├── Full_stack.py
│   └── Javascript.py
├── Data/                 # Sample datasets
├── .streamlit/           # Streamlit configuration
├── static_index.html     # Static version for Netlify
└── netlify.toml         # Netlify configuration
```

## 🔐 Security

- Password protection enabled (default: `admin123`)
- Environment variables for sensitive data
- Secure API key management

## 📊 Technologies Used

- **Frontend**: Streamlit, HTML, CSS
- **Backend**: Python
- **ML/AI**: scikit-learn, OpenAI, Google Generative AI
- **Cloud**: AWS (boto3)
- **DevOps**: Docker, Kubernetes, Jenkins
- **Database**: SQLAlchemy, MongoDB, PostgreSQL

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the configuration files

---

**Built with ❤️ using Streamlit**
