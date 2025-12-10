# Quick Start Guide

Get LensLock Pro running in 5 minutes!

## Step 1: Prerequisites

Make sure you have:
- Python 3.11+ installed
- A Supabase account (free tier is fine)

## Step 2: Get Supabase Credentials

1. Go to https://supabase.com and create a free account
2. Create a new project
3. Go to Project Settings > API
4. Copy your:
   - Project URL
   - Anon/Public key

## Step 3: Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a virtual environment
- Install all dependencies
- Set up required directories
- Create .env file template

## Step 4: Configure Environment

Edit the `.env` file and add your Supabase credentials:

```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

## Step 5: Start the Server

```bash
npm run dev
```

The application will start at http://localhost:8000

## Step 6: Try It Out!

1. Open http://localhost:8000 in your browser
2. Register a missing person with their photo
3. Upload a test video
4. Watch the AI detect and highlight the person!

## Troubleshooting

### "Module not found" errors
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Database connection errors
- Verify your Supabase credentials in `.env`
- Check that your Supabase project is active

### Video processing is slow
- Try using shorter videos (< 30 seconds) for testing
- Reduce video resolution before uploading
- Consider using a machine with more CPU cores

## What's Next?

- Check out ARCHITECTURE.md to understand the system
- Read DEPLOYMENT.md for production deployment
- Browse the code in backend/ to customize detection

## Need Help?

- Check the main README.md for full documentation
- Review API endpoints in backend/main.py
- See detection logic in backend/detection.py

Happy detecting!
