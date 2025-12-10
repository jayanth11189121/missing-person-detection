# Deployment Guide

## Prerequisites

Before deploying, ensure you have:

1. A Supabase account with a project created
2. Database migrations applied
3. Environment variables configured

## Supabase Setup

1. Create a new Supabase project at https://supabase.com
2. Navigate to Project Settings > API
3. Copy your Project URL and Anon Key
4. The database migrations are automatically applied via the Supabase MCP tools

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Supabase credentials:
   ```
   VITE_SUPABASE_URL=your_project_url
   VITE_SUPABASE_ANON_KEY=your_anon_key
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Access the application at http://localhost:8000

## Deploy to Heroku

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables:
   ```bash
   heroku config:set VITE_SUPABASE_URL=your_url
   heroku config:set VITE_SUPABASE_ANON_KEY=your_key
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

## Deploy to Vercel

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy:
   ```bash
   vercel
   ```

4. Set environment variables in Vercel dashboard:
   - Go to Project Settings > Environment Variables
   - Add VITE_SUPABASE_URL
   - Add VITE_SUPABASE_ANON_KEY

## Deploy to Railway

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login and initialize:
   ```bash
   railway login
   railway init
   ```

3. Add environment variables:
   ```bash
   railway variables set VITE_SUPABASE_URL=your_url
   railway variables set VITE_SUPABASE_ANON_KEY=your_key
   ```

4. Deploy:
   ```bash
   railway up
   ```

## Environment Variables Required

- `VITE_SUPABASE_URL` - Your Supabase project URL
- `VITE_SUPABASE_ANON_KEY` - Your Supabase anonymous key

## Post-Deployment Checklist

- [ ] Verify database connection works
- [ ] Test person registration
- [ ] Test video upload and detection
- [ ] Check file storage paths are working
- [ ] Verify API endpoints are accessible
- [ ] Test CORS headers for frontend
- [ ] Monitor application logs
- [ ] Set up error tracking

## Troubleshooting

### Database Connection Errors
- Verify Supabase credentials are correct
- Check if database migrations have been applied
- Ensure Row Level Security policies are configured

### File Upload Issues
- Verify upload directories exist and have write permissions
- Check file size limits on your hosting platform
- Ensure supported video formats are being used

### Performance Issues
- Consider using a GPU-enabled hosting service for faster processing
- Optimize frame skip settings for faster video processing
- Implement background job processing for long videos

## Scaling Considerations

For production use:
- Add Redis for caching and job queues
- Implement CDN for static file serving
- Use cloud storage (AWS S3, Cloudinary) for uploads
- Add rate limiting to prevent abuse
- Implement user authentication
- Set up monitoring and alerting
