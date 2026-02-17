# 🚀 Start the Frontend

The backend is already running on **http://localhost:8000** ✅

## To start the frontend:

Open a **NEW terminal window** and run:

```bash
cd /Users/hisan/Desktop/Data/Projects/TravelAgent/frontend
npm install
npm start
```

The frontend will open automatically at **http://localhost:3000**

## If npm is not found:

If you get "npm: command not found", you may need to:

1. **Add Node to your PATH:**
   ```bash
   # For bash/zsh
   export PATH="/usr/local/bin:$PATH"
   ```

2. **Or find where Node is installed:**
   ```bash
   which node
   which npm
   ```

3. **Or use nvm if installed:**
   ```bash
   nvm use node
   ```

## Already have Node in PATH?

If Node/npm are already in your PATH, just run:

```bash
cd frontend
npm start
```

That's it! The app will open in your browser automatically.

---

**Quick Check:**
- ✅ Backend running: http://localhost:8000
- ✅ Backend health: http://localhost:8000/api/v1/health
- ✅ API docs: http://localhost:8000/docs
- ⏳ Frontend: Will be at http://localhost:3000 once you start it
