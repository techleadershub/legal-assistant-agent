# 🚀 Streamlit Cloud Deployment Guide

This guide will help you deploy your Legal Assistant Agent to Streamlit Cloud.

## 📋 Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **Google API Key**: Get one from [Google AI Studio](https://makersuite.google.com/app/apikey)
3. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)

## 🔧 Pre-Deployment Setup

### 1. Repository Structure
Ensure your repository has these files:
```
Legal Assistant Agent/
├── app.py                     # Main Streamlit app
├── requirements.txt           # Dependencies
├── .streamlit/
│   ├── config.toml           # Streamlit configuration
│   └── secrets.toml          # Secrets template (don't commit!)
├── .gitignore                # Git ignore file
├── src/                      # Source code
├── data/                     # Sample documents
└── DEPLOYMENT.md             # This file
```

### 2. Environment Variables
The app is configured to work with both:
- **Local development**: `.env` file
- **Streamlit Cloud**: Secrets management

## 🚀 Deployment Steps

### Step 1: Push to GitHub
1. Commit all your changes:
   ```bash
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Connect your GitHub repository
4. Set the following:
   - **Repository**: `your-username/your-repo-name`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom URL (optional)

### Step 3: Configure Secrets
1. In your Streamlit Cloud app dashboard, go to "Settings" → "Secrets"
2. Add your secrets in TOML format:
   ```toml
   GOOGLE_API_KEY = "your_actual_google_api_key_here"
   ```

### Step 4: Deploy
1. Click "Deploy!"
2. Wait for the deployment to complete (usually 2-5 minutes)
3. Your app will be available at the provided URL

## 🔑 Getting a Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key
4. Add it to Streamlit Cloud secrets (never commit it to GitHub!)

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
- **Issue**: Module not found errors
- **Solution**: Check `requirements.txt` has all dependencies

#### 2. API Key Not Found
- **Issue**: "Google API Key not found" error
- **Solution**: Verify the key is added to Streamlit Cloud secrets

#### 3. Memory Issues
- **Issue**: App crashes due to memory limits
- **Solution**: Streamlit Cloud has resource limits. The app is optimized with caching.

#### 4. PDF Processing Fails
- **Issue**: Large PDFs fail to process
- **Solution**: File size is limited to 10MB for cloud deployment

#### 5. Model Not Found
- **Issue**: Gemini model errors
- **Solution**: App uses `gemini-2.0-flash-exp` - ensure your API key has access

### Performance Optimization

The app includes several optimizations for cloud deployment:

1. **Caching**: `@st.cache_resource` for vector store manager
2. **Error Handling**: Comprehensive error handling and user feedback
3. **Resource Management**: File size limits and retry logic
4. **Fallback Options**: Simple vector store if FAISS fails

## 📊 Monitoring

### App Health
Monitor your app's performance in the Streamlit Cloud dashboard:
- **Logs**: Check for errors and warnings
- **Metrics**: Monitor resource usage
- **Uptime**: Track availability

### Usage Limits
Be aware of:
- **Google API**: Rate limits and quotas
- **Streamlit Cloud**: Resource and bandwidth limits
- **File Uploads**: 10MB limit per file

## 🔄 Updates and Maintenance

### Updating Your App
1. Make changes to your code locally
2. Test thoroughly
3. Commit and push to GitHub
4. Streamlit Cloud will automatically redeploy

### Managing Dependencies
- Keep `requirements.txt` updated
- Test new dependencies locally first
- Monitor for security updates

## 🛡️ Security Best Practices

1. **Never commit secrets** to your repository
2. **Use environment variables** for all sensitive data
3. **Keep dependencies updated** for security patches
4. **Monitor API usage** to prevent abuse
5. **Use .gitignore** to exclude sensitive files

## 📱 Mobile Optimization

The app is designed to work on mobile devices with:
- Responsive design
- Touch-friendly interface
- Optimized layouts for small screens

## 🎯 Production Tips

1. **Test thoroughly** before deploying
2. **Monitor logs** regularly
3. **Set up alerts** for critical errors
4. **Have a rollback plan** ready
5. **Document any customizations**

## 📞 Support

If you encounter issues:

1. Check the [Streamlit Documentation](https://docs.streamlit.io)
2. Visit [Streamlit Community Forum](https://discuss.streamlit.io)
3. Check GitHub Issues for known problems
4. Review app logs in Streamlit Cloud dashboard

## 🎉 Success!

Once deployed, your Legal Assistant Agent will be available 24/7 at your Streamlit Cloud URL. Share it with users and enjoy your AI-powered legal document analyzer!

---

**Note**: This deployment guide assumes you're using the free tier of Streamlit Cloud. For production applications with high traffic, consider upgrading to Streamlit Cloud for Teams.
