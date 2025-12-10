# LensLock Architecture

## System Overview

LensLock is a missing person detection system that uses facial recognition to identify individuals in uploaded videos.

## Architecture Diagram

```
┌─────────────────┐
│   Web Browser   │
│   (Frontend)    │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────▼────────┐
│   FastAPI       │
│   Backend       │
│                 │
│  - API Routes   │
│  - File Upload  │
│  - Detection    │
└────┬───────┬────┘
     │       │
     │       │
     │       └──────────────┐
     │                      │
┌────▼────────┐      ┌─────▼──────────┐
│  Supabase   │      │   DeepFace     │
│  Database   │      │   AI/ML        │
│             │      │                │
│ - Persons   │      │ - Face Extract │
│ - Detections│      │ - Recognition  │
│ - Reports   │      │ - Embeddings   │
└─────────────┘      └────────────────┘
```

## Component Details

### Frontend (public/)

**Technology**: Vanilla JavaScript, HTML5, CSS3

**Files**:
- `index.html` - Main application structure
- `styles.css` - Styling and responsive design
- `app.js` - Client-side logic and API integration

**Features**:
- Person registration form
- Video upload interface
- Detection results display
- Detection history viewer
- Responsive design with dark mode

### Backend (backend/)

**Technology**: FastAPI (Python)

**Files**:
- `main.py` - API routes and server configuration
- `detection.py` - Face detection and recognition logic
- `database.py` - Supabase database operations

**Key Endpoints**:
- `POST /api/missing-persons` - Register new missing person
- `GET /api/missing-persons` - List all registered persons
- `POST /api/detect/video` - Detect person in uploaded video
- `GET /api/detections/{person_id}` - Get detections for a person

### AI/ML Pipeline

**Model**: DeepFace with Facenet

**Process Flow**:
1. Extract reference face embedding from uploaded image
2. Process video frame by frame
3. Extract faces from each frame
4. Calculate similarity between reference and detected faces
5. Mark detection if similarity > threshold (0.7)
6. Annotate detected frames with bounding boxes
7. Generate output video with highlights

**Optimizations**:
- Frame skipping (process every 5th frame)
- Image downscaling for faster processing
- Early termination after detection
- Result caching

### Database Schema

**Tables**:

1. `missing_persons`
   - Stores registered missing persons
   - Reference images
   - Status tracking

2. `detections`
   - Individual detection records
   - Links to missing persons
   - Confidence scores
   - Timestamps

3. `detection_reports`
   - Aggregated reports
   - Export data
   - PDF generation metadata

### File Storage

**Directories**:
- `uploads/` - Reference images and uploaded videos
- `outputs/` - Processed videos and detected frames

**Note**: In production, use cloud storage (S3, GCS, Cloudinary)

## Data Flow

### Person Registration
```
User Input → Frontend Form → POST /api/missing-persons →
Backend Validation → Save Image → Database Insert →
Success Response → UI Update
```

### Video Detection
```
User Upload Video → POST /api/detect/video →
Load Reference Image → Extract Embedding →
Process Video Frame-by-Frame →
  ├─ Extract Faces
  ├─ Calculate Similarity
  └─ Mark Detections
Generate Output Video → Save Results →
Database Insert → Return Detection Data →
Display Results to User
```

## Security

### Authentication
- Currently public API
- Recommended: Add JWT authentication for production

### Row Level Security (RLS)
- Enabled on all Supabase tables
- Policies configured for authenticated users
- Public read access for active missing persons

### File Upload Security
- File type validation
- Size limits enforced
- Sanitized file names
- Isolated storage directories

## Performance Considerations

### Current Implementation
- Frame skip: 5 frames (reduces processing by 80%)
- Image downscaling: 50% for face detection
- Threshold: 0.7 for reliable matches

### Bottlenecks
- Video processing is CPU-intensive
- Face detection on every frame
- Embedding calculation per face
- Video encoding for output

### Optimization Strategies
1. GPU acceleration for DeepFace
2. Background job processing
3. Result caching
4. Parallel video processing
5. Lower resolution output videos

## Deployment Architecture

### Recommended Setup

```
┌──────────────┐
│   CDN        │ (Static Assets)
└──────┬───────┘
       │
┌──────▼───────┐
│  Load        │
│  Balancer    │
└──────┬───────┘
       │
       ├─────────┬─────────┐
       │         │         │
┌──────▼──┐ ┌───▼────┐ ┌──▼──────┐
│ Server 1│ │Server 2│ │Server 3│
└────┬────┘ └───┬────┘ └────┬────┘
     │          │           │
     └──────────┴───────────┘
                │
     ┌──────────▼───────────┐
     │   Supabase Cloud     │
     │   (Database)         │
     └──────────────────────┘
```

## Future Enhancements

1. **Real-time Processing**
   - WebSocket support
   - Live camera feeds
   - RTSP stream handling

2. **Advanced Detection**
   - Multiple face tracking
   - Age progression models
   - Clothing/attribute recognition

3. **Scalability**
   - Microservices architecture
   - Message queue for jobs
   - Distributed processing

4. **User Features**
   - Authentication system
   - User dashboards
   - Email notifications
   - Mobile applications
