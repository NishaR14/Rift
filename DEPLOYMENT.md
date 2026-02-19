# Deployment Guide

## Quick Start

### Local Development

1. **Backend Setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python app.py
```

2. **Frontend Setup** (in new terminal):
```bash
npm install
npm run dev
```

3. Access application at `http://localhost:3000`

## Deployment Options

### Option 1: Vercel (Frontend) + Render (Backend)

#### Frontend (Vercel)
1. Push code to GitHub
2. Connect repository to Vercel
3. Set build command: `npm run build`
4. Set output directory: `.next`
5. Add environment variable: `NEXT_PUBLIC_BACKEND_URL=https://your-backend.onrender.com`

#### Backend (Render)
1. Create new Web Service on Render
2. Connect GitHub repository
3. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python backend/app.py`
4. Add environment variable: `OPENAI_API_KEY=your_key`

### Option 2: Netlify (Frontend) + Railway (Backend)

#### Frontend (Netlify)
1. Connect GitHub repo
2. Build command: `npm run build`
3. Publish directory: `.next`
4. Add environment variable: `NEXT_PUBLIC_BACKEND_URL`

#### Backend (Railway)
1. Create new project
2. Connect GitHub repo
3. Railway auto-detects Python
4. Add environment variables in dashboard

### Option 3: Full Stack on Vercel

1. Use Vercel Serverless Functions for API
2. Convert Flask routes to Vercel API routes
3. Single deployment

## Environment Variables

### Backend
- `OPENAI_API_KEY`: Your OpenAI API key

### Frontend
- `NEXT_PUBLIC_BACKEND_URL`: Backend API URL (default: http://localhost:5000)

## Testing Deployment

1. Upload sample VCF file from `test_data/` directory
2. Enter drug name: `CODEINE`
3. Verify JSON output matches schema
4. Test multiple drugs: `WARFARIN, CLOPIDOGREL`

## Troubleshooting

- **CORS errors**: Ensure backend CORS is configured for frontend domain
- **File upload fails**: Check file size limits (5MB max)
- **LLM errors**: Verify OpenAI API key is set correctly
- **Build fails**: Check Node.js version (18+) and Python version (3.8+)
