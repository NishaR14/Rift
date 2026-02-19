# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ Node.js 18+ installed
- ✅ OpenAI API key (for LLM explanations)

### Step 1: Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r ../requirements.txt

# Set up environment
cd ..
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run backend
cd backend
python app.py
```

Backend runs on `http://localhost:5000`

### Step 2: Frontend Setup (2 minutes)

```bash
# In project root (new terminal)
npm install

# Run frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

### Step 3: Test the Application (1 minute)

1. Open `http://localhost:3000` in browser
2. Upload `test_data/sample_patient.vcf`
3. Enter drug: `CODEINE`
4. Click "Analyze Pharmacogenomic Risk"
5. View results!

## 📝 Testing with Sample Files

Use the provided test VCF files:
- `test_data/sample_patient.vcf` - Normal metabolizer
- `test_data/sample_pm_patient.vcf` - Poor metabolizer

## 🔧 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version`
- Ensure virtual environment is activated
- Install dependencies: `pip install -r requirements.txt`

**Frontend won't start:**
- Check Node version: `node --version`
- Clear cache: `rm -rf node_modules .next && npm install`
- Check port 3000 is available

**API errors:**
- Verify backend is running on port 5000
- Check CORS settings
- Verify environment variables are set

## 📚 Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions
- Review API documentation in README.md
