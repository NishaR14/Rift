# Running PharmaGuard in VS Code

## 🚀 Quick Start in VS Code

### Method 1: Using Launch Configurations (Recommended)

1. **Open the project in VS Code**
   ```bash
   code .
   ```

2. **Install Required Extensions** (if not already installed):
   - Python (Microsoft)
   - ESLint
   - Prettier
   - Tailwind CSS IntelliSense

3. **Set Up Backend**:
   - Open terminal in VS Code (`Ctrl + ~` or `View > Terminal`)
   - Run these commands:
   ```bash
   cd backend
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   
   pip install -r ../requirements.txt
   ```

4. **Set Up Frontend**:
   - In the same or new terminal:
   ```bash
   npm install
   ```

5. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`
   - Add your `OPENAI_API_KEY`

6. **Run the Application**:
   - Press `F5` or go to `Run > Start Debugging`
   - Select **"Run Full Stack (Backend + Frontend)"** from the dropdown
   - Or run individually:
     - **"Python: Flask Backend"** - Runs backend only
     - **"Next.js: Frontend"** - Runs frontend only

### Method 2: Using Tasks

1. **Open Command Palette** (`Ctrl + Shift + P`)

2. **Run Tasks**:
   - Type: `Tasks: Run Task`
   - Select: **"Run Full Stack"**
   - This will start both backend and frontend in parallel

### Method 3: Manual Terminal Commands

1. **Open Integrated Terminal** (`Ctrl + ~`)

2. **Terminal 1 - Backend**:
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   # or: source venv/bin/activate  # Mac/Linux
   python app.py
   ```

3. **Terminal 2 - Frontend** (Split terminal or new terminal):
   ```bash
   npm run dev
   ```

## 📋 VS Code Features

### Debugging

- **Backend Debugging**: Set breakpoints in Python files, use the "Python: Flask Backend" configuration
- **Frontend Debugging**: Set breakpoints in TypeScript/React files, use Chrome DevTools

### Integrated Terminal

- Use split terminals to run both servers simultaneously
- Right-click terminal tab → "Split Terminal"

### File Watching

- VS Code automatically watches for file changes
- Both Flask and Next.js support hot-reload

## 🔧 Troubleshooting

### Python Not Found
- Install Python extension
- Set Python interpreter: `Ctrl + Shift + P` → "Python: Select Interpreter"
- Choose the venv interpreter: `backend/venv/Scripts/python.exe`

### Port Already in Use
- Backend (5000): Change port in `backend/app.py`
- Frontend (3000): Change port in `package.json` scripts

### Module Not Found Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- For frontend: `npm install`

### CORS Errors
- Ensure backend is running on port 5000
- Check `backend/app.py` has `CORS(app)` enabled

## 🎯 Recommended VS Code Extensions

- **Python** (ms-python.python)
- **ESLint** (dbaeumer.vscode-eslint)
- **Prettier** (esbenp.prettier-vscode)
- **Tailwind CSS IntelliSense** (bradlc.vscode-tailwindcss)
- **GitLens** (eamodio.gitlens)
- **Error Lens** (usernamehw.errorlens)

## 📝 Keyboard Shortcuts

- `F5` - Start Debugging
- `Ctrl + Shift + P` - Command Palette
- `Ctrl + ~` - Toggle Terminal
- `Ctrl + B` - Toggle Sidebar
- `Ctrl + Shift + E` - Explorer

## 🚀 Quick Commands

### Install Everything
```bash
# Backend
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r ../requirements.txt

# Frontend
npm install
```

### Run Everything
Press `F5` and select "Run Full Stack (Backend + Frontend)"

### Test the Application
1. Open browser: `http://localhost:3000`
2. Upload `test_data/sample_patient.vcf`
3. Enter drug: `CODEINE`
4. Click "Analyze Pharmacogenomic Risk"
