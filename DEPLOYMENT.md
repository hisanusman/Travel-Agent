# 🚀 Deployment Guide

## Vercel Deployment

### Prerequisites

1. Vercel account (https://vercel.com)
2. Vercel CLI installed: `npm install -g vercel`
3. GitHub repository (optional but recommended)

### Step 1: Prepare for Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login
```

### Step 2: Configure Environment Variables

In Vercel dashboard or CLI, add these secrets:

```bash
vercel secrets add google_api_key "your-google-api-key"
vercel secrets add openai_api_key "your-openai-api-key"
vercel secrets add pinecone_api_key "your-pinecone-api-key"
```

### Step 3: Deploy Backend

```bash
# From project root
vercel --prod
```

### Step 4: Deploy Frontend

```bash
# Build frontend
cd frontend
npm run build

# The frontend will be deployed as part of the Vercel build
```

### Step 5: Configure Custom Domain (Optional)

In Vercel dashboard:
1. Go to your project settings
2. Navigate to "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

## Alternative Deployment Options

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build -d

# Check logs
docker-compose logs -f

# Stop containers
docker-compose down
```

### AWS Elastic Beanstalk

1. Install AWS CLI and EB CLI
2. Initialize EB application:
   ```bash
   eb init -p python-3.11 travel-agent
   ```
3. Create environment:
   ```bash
   eb create travel-agent-env
   ```
4. Deploy:
   ```bash
   eb deploy
   ```

### Google Cloud Run

```bash
# Build container
docker build -t gcr.io/[PROJECT-ID]/travel-agent .

# Push to Container Registry
docker push gcr.io/[PROJECT-ID]/travel-agent

# Deploy to Cloud Run
gcloud run deploy travel-agent \
  --image gcr.io/[PROJECT-ID]/travel-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create travel-agent-app

# Set environment variables
heroku config:set GOOGLE_API_KEY=your-key
heroku config:set OPENAI_API_KEY=your-key
heroku config:set PINECONE_API_KEY=your-key

# Deploy
git push heroku main
```

## Production Checklist

### Before Deployment

- [ ] All API keys configured as environment variables
- [ ] Database migrations tested
- [ ] Frontend build successful (`npm run build`)
- [ ] Backend tests passing
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] CORS settings verified
- [ ] Rate limiting configured (if needed)

### After Deployment

- [ ] Health endpoint responding (`/api/v1/health`)
- [ ] API documentation accessible (`/docs`)
- [ ] Frontend loads correctly
- [ ] Create a test travel plan
- [ ] Export functionality works
- [ ] Database persistence verified
- [ ] Monitor error logs
- [ ] Set up alerting (optional)

## Monitoring & Maintenance

### Logging

The application uses Loguru for logging. To view logs:

**Docker:**
```bash
docker-compose logs -f backend
```

**Vercel:**
Check the Vercel dashboard under "Deployments" → "Logs"

### Health Checks

Monitor the health endpoint:
```bash
curl https://your-domain.com/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2026-02-17T..."
}
```

### Database Backups

For SQLite in production:
```bash
# Backup
sqlite3 travel_agent.db ".backup travel_agent_backup.db"

# Restore
sqlite3 travel_agent.db ".restore travel_agent_backup.db"
```

## Scaling Considerations

### Database

- Consider migrating to PostgreSQL for production
- Implement connection pooling
- Set up read replicas for high traffic

### API

- Implement caching (Redis)
- Add rate limiting (per user/IP)
- Use CDN for static assets
- Enable compression

### Agents

- Implement request queuing
- Add timeout handling
- Cache frequent queries
- Monitor API usage costs

## Cost Optimization

### API Usage

- Monitor Google API calls
- Implement request caching
- Set usage limits
- Use batch processing where possible

### Infrastructure

- Use serverless for variable workload
- Implement auto-scaling
- Optimize cold starts
- Monitor resource usage

## Security Hardening

### Production Security

- [ ] Enable HTTPS only
- [ ] Implement authentication
- [ ] Add request signing
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable audit logging
- [ ] Implement input validation
- [ ] Add CSRF protection
- [ ] Set security headers

### API Keys

- Rotate keys regularly
- Use separate keys for dev/prod
- Monitor for leaked keys
- Implement key rotation strategy

## Troubleshooting

### Common Issues

**Backend won't start:**
- Check environment variables
- Verify Python version compatibility
- Review error logs

**Frontend 404 errors:**
- Verify build output directory
- Check routing configuration
- Ensure static files are served

**API timeouts:**
- Increase timeout limits
- Check agent response times
- Monitor external API latency

**Database errors:**
- Verify connection string
- Check database permissions
- Review migration status

## Support & Resources

- **Documentation:** AGENTS.md
- **Setup Guide:** README_SETUP.md
- **API Docs:** https://your-domain.com/docs
- **Issues:** Report in repository

---

*Deployment Guide - Last updated: February 17, 2026*
