# Vercel Deployment Guide for Akulearn Backend

## Overview

This guide provides step-by-step instructions for deploying the Akulearn backend to Vercel, including proper configuration of requirements.txt, .gitignore, and .vercelignore files. All commits should be made directly to the main branch.

## Prerequisites

- Vercel account
- Git installed
- Python 3.9 or higher
- Access to the Akulearn repository

---

## Step 1: Create Backend requirements.txt for Vercel

### 1.1 Create requirements.txt in Backend Directory

Create a `requirements.txt` file in your backend directory with the following dependencies. This file is essential for Vercel to install the correct Python packages during deployment.

```
txt
# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Authentication
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
alembic==1.13.1
psycopg2-binary==2.9.9

# HTTP Client
httpx==0.26.0
requests==2.31.0

# Utilities
pydantic==2.5.3
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Logging
loguru==0.7.2

# Date/Time
python-dateutil==2.8.2

# Validation
email-validator==2.1.0.post1

# CORS
starlette==0.35.1
```

### 1.2 Verify requirements.txt Location

Ensure the `requirements.txt` file is placed in the root of your backend directory. Vercel automatically detects this file and installs dependencies during deployment.

```
akulearn_backend/
├── requirements.txt  # This file
├── main.py
├── api/
├── services/
└── models/
```

---

## Step 2: Configure vercel.json

### 2.1 Create vercel.json Configuration File

Create a `vercel.json` file in the root of your backend project to configure the Vercel deployment:

```
json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.9"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

### 2.2 Alternative Configuration for Multiple Services

If you have multiple microservices, create separate configuration:

```
json
{
  "version": 2,
  "builds": [
    {
      "src": "api_gateway/main.py",
      "use": "@vercel/python",
      "config": {
        "runtime": "python3.9",
        "maxLambdaSize": "15mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api_gateway/main.py"
    }
  ]
}
```

---

## Step 3: Update .gitignore

### 3.1 Improved .gitignore for Vercel Deployment

Update your `.gitignore` file to exclude unnecessary files while keeping only what's needed for deployment:

```
gitignore
# Node.js (if used)
node_modules/
npm-debug.log
yarn-error.log

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
env/
venv/
.venv/
myenv/
*.egg-info/
dist/
build/

# Virtual Environment
venv/
ENV/
env/

# Logs and temporary outputs
*.log
pyarrow-install.log
ps-output.txt
pull-output.txt
docker-info.txt
docker-ps-all.txt
docker-version.txt
logs-*.txt
*.out
*.err

# Editor/IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment variables (keep .env.example but not .env)
.env
.env.local
.env.*.local

# Database
*.db
*.sqlite
*.sqlite3

# Build artifacts
*.egg
*.whl
*.tar.gz

# Test coverage
.coverage
htmlcov/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints/

# Misc
*.zip
*.tar
*.gz
```

### 3.2 Key Changes Made

The improved `.gitignore` includes:

- **Python virtual environments**: Excludes `venv/`, `env/`, `.venv/` to prevent uploading large virtual environments
- **Build artifacts**: Excludes `dist/`, `build/`, `*.egg` to keep the repository clean
- **Cache files**: Excludes `__pycache__/`, `.pytest_cache/` to reduce repository size
- **Environment files**: Excludes `.env` files but allows `.env.example` for reference
- **Database files**: Excludes local database files that shouldn't be committed

---

## Step 4: Create .vercelignore

### 4.1 Create .vercelignore File

Create a `.vercelignore` file in the root of your project to exclude files that shouldn't be deployed to Vercel:

```
vercelignore
# Version Control
.git
.gitignore
.gitattributes

# Documentation (keep if needed for reference)
*.md
!README.md
docs/
LICENSE

# Configuration files (keep vercel.json)
*.json
!vercel.json
!package.json

# Environment and secrets
.env
.env.local
.env.*.local
*.pem
*.key

# Local development files
.dockerignore
.docker/
docker-compose*
Dockerfile*

# Build and cache
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
htmlcov/

# Virtual environments
venv/
env/
.venv/
myenv/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db

# Test and development files
test/
tests/
*_test.py
*_tests.py
conftest.py

# Logs
*.log
logs/

# Temporary files
tmp/
temp/
*.tmp

# Large media files (if not needed for deployment)
# generated_assets/
# generated_images/
# videos/
```

### 4.2 What to Include in .vercelignore

The `.vercelignore` file should exclude:

- **Git files**: `.git/` directory and git-related files
- **Development files**: IDE settings, temporary files
- **Testing files**: Test directories and test configuration
- **Documentation**: Markdown files (except README)
- **Environment secrets**: `.env` files containing sensitive data
- **Large media files**: Generated assets that aren't needed for the backend
- **Build caches**: Python cache files that will be regenerated

---

## Step 5: Deploy to Vercel

### 5.1 Install Vercel CLI (Optional)

```
bash
npm install -g vercel
```

### 5.2 Deploy from Command Line

```
bash
# Navigate to your backend directory
cd connected_stack/backend

# Login to Vercel (if not already logged in)
vercel login

# Deploy to Vercel
vercel
```

### 5.3 Deploy via Git Integration

1. Push your code to GitHub/GitLab/Bitbucket
2. Import the project in Vercel
3. Configure the following settings:
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
   - Install Command: `pip install -r requirements.txt`

### 5.4 Environment Variables

Set the following environment variables in the Vercel dashboard:

```
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Step 6: Commit to Main Branch

### 6.1 Commit the Changes

Following the project's commit guide, commit all the changes to the main branch:

```
bash
# Stage all changes
git add .

# Commit with descriptive message
git commit -m "feat: Configure Vercel deployment for backend

- Add requirements.txt with FastAPI and dependencies
- Create vercel.json configuration
- Update .gitignore for Python and Vercel
- Add .vercelignore for deployment exclusions
- Configure environment variables for production

Deployment configuration:
- Python 3.9 runtime
- FastAPI framework
- Uvicorn ASGI server
- Environment-based configuration"
```

### 6.2 Push to Remote

```
bash
# Push directly to main branch
git push origin main
```

### 6.3 Alternative: Use Feature Branch

If you prefer using feature branches:

```
bash
# Create feature branch
git checkout -b feat/vercel-backend-deployment

# Make your changes and commit
git add .
git commit -m "feat: Configure Vercel deployment for backend"

# Push the branch
git push origin feat/vercel-backend-deployment

# Create pull request and merge to main
# Then push to production
git checkout main
git pull origin main
git push origin main
```

---

## Step 7: Verify Deployment

### 7.1 Check Deployment Status

After pushing to main, check the Vercel dashboard for deployment status. The deployment should start automatically.

### 7.2 Test the API

Once deployed, test your API endpoints:

```bash
# Get the deployment URL from Vercel dashboard
# Test health check endpoint
curl https://your-project.vercel.app/health

# Test API endpoint
curl https://your-project.vercel.app/api/lessons
```

### 7.3 Monitor Logs

Check Vercel function logs for any errors:

```
bash
vercel logs your-project
```

---

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure all dependencies are in `requirements.txt`
2. **Import errors**: Check Python path configuration in `vercel.json`
3. **Timeout errors**: Increase timeout in Vercel dashboard settings
4. **Environment variables**: Ensure all required env vars are set in Vercel

### Performance Optimization

- Use `@vercel/python` for Python functions
- Enable edge caching for static content
- Use database connection pooling
- Implement lazy loading for heavy dependencies

---

## Additional Resources

- [Vercel Python Runtime Documentation](https://vercel.com/docs/serverless-functions/runtimes/python)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/de/)
- [Vercel Environment Variables](https://vercel.com/docs/environment-variables)

---

**Last Updated**: 2024
**Main Branch**: All production deployments go to main branch
