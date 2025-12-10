# LensLock Pro - Missing Person Detection System

Advanced AI-powered missing person detection system using facial recognition and video analysis.

## Features

- **Person Registration**: Upload reference images of missing persons
- **Video Detection**: Analyze videos to detect registered missing persons
- **Real-time Processing**: Fast face detection and recognition using DeepFace
- **Detection History**: Track all detections with timestamps and confidence scores
- **Modern UI**: Clean, responsive web interface with dark mode
- **Database Integration**: Supabase backend for persistent storage
- **Report Generation**: Generate detection reports

## Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **AI/ML**: DeepFace, OpenCV
- **Database**: Supabase (PostgreSQL)
- **Face Recognition**: Facenet model

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Supabase account

### Installation

1. Clone the repository and navigate to the project directory

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials:
     ```
     VITE_SUPABASE_URL=your_supabase_project_url
     VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
     ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:8000`

## Usage

### Register a Missing Person

1. Navigate to the Upload section
2. Enter the person's name and description
3. Upload a clear reference image
4. Click "Register Person"

### Detect in Video

1. Select a registered missing person from the dropdown
2. Upload a video file
3. Click "Start Detection"
4. Wait for processing to complete
5. View results with confidence scores

### View Detections

1. Click on "Detections" in the navigation
2. Browse all detected matches
3. View confidence scores and timestamps

## API Endpoints

- `GET /` - API status
- `GET /api/missing-persons` - List all missing persons
- `POST /api/missing-persons` - Register new missing person
- `POST /api/detect/video` - Detect person in video
- `GET /api/detections/{person_id}` - Get detections for a person
- `GET /api/health` - Health check

## Deployment

### Heroku

```bash
heroku create your-app-name
heroku config:set VITE_SUPABASE_URL=your_url
heroku config:set VITE_SUPABASE_ANON_KEY=your_key
git push heroku main
```

### Vercel

```bash
vercel deploy
```

Make sure to add environment variables in your Vercel dashboard.

## Performance Notes

- Frame skip optimization reduces processing time
- Confidence threshold set to 70% for reliable matches
- Supports multiple video formats (MP4, AVI, MOV)
- Automatic video compression for faster processing

## Future Enhancements

- Live webcam detection
- RTSP stream support
- Multiple face tracking in single frame
- PDF report generation
- Email notifications on detection
- Mobile app integration

## License

MIT License
