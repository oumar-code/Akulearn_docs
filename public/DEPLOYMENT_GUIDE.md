# Akudemy Static Site Deployment Guide

## 📁 Project Structure

```
public/
├── index.html          (landing page)
├── about.html          (about page)
├── blog.html           (blog page)
├── pricing.html        (pricing page)
└── vercel.json         (deployment config)
```

## 🚀 Deployment Instructions

### Option 1: Deploy to Vercel (Recommended)

**1. Create Vercel Account** (Free)
- Go to vercel.com
- Sign up with GitHub, GitLab, or email

**2. Push to GitHub**
```bash
cd /path/to/Akulearn_docs
git init
git add .
git commit -m "Add Akudemy static site"
git remote add origin https://github.com/yourusername/akudemy-site.git
git push -u origin main
```

**3. Import on Vercel**
- Go to vercel.com/dashboard
- Click "Add New..." → "Project"
- Import your GitHub repository
- Root Directory: `public`
- Click Deploy

**✅ Done!** Your site is live at `akudemy.vercel.app`

### Option 2: Deploy to Netlify

**1. Create Netlify Account** (Free)
- Go to netlify.com
- Sign up

**2. Connect Repository**
- Click "New site from Git"
- Select GitHub
- Choose your repository
- Set Build Command: (leave blank - static site)
- Set Publish Directory: `public`
- Deploy

**3. Custom Domain**
- Go to Domain Settings
- Add your custom domain (akudemy.com)
- Update DNS records

### Option 3: Manual Deployment

**Using surge.sh** (Quick & Easy)
```bash
npm install -g surge
cd public
surge
```

**Using GitHub Pages**
```bash
# Push to gh-pages branch
git subtree push --prefix public origin gh-pages
```

## 🔗 Connect Your Domain

### If using Vercel
1. Go to Project Settings → Domains
2. Add your domain: `akudemy.com`
3. Follow DNS configuration instructions
4. Update your domain registrar nameservers

### If using Netlify
1. Go to Domain Settings
2. Add custom domain
3. Update DNS records at your registrar

## 📊 Environment Setup

No environment variables needed! This is a static site. All content is hardcoded in HTML.

## 🔄 Making Updates

**To update content:**
1. Edit HTML files in `/public/`
2. Commit and push to GitHub
3. Vercel/Netlify auto-deploys

**To add new pages:**
1. Create `new-page.html` in `/public/`
2. Add navigation links to `index.html`, `about.html`, etc.
3. Push to GitHub
4. Auto-deployed

## 📱 SEO & Performance

**Current Status:**
- ✅ Mobile-responsive
- ✅ Fast load time (<1s)
- ✅ SEO meta tags included
- ✅ Social media open graph tags
- ✅ Security headers enabled

## 🛡️ Security

Vercel automatically provides:
- ✅ HTTPS/SSL encryption
- ✅ DDoS protection
- ✅ Security headers
- ✅ 99.99% uptime SLA

## 📈 Analytics

Add Google Analytics (optional):
1. Create Google Analytics account
2. Get your tracking ID
3. Add this to `<head>` of each HTML file:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_ID');
</script>
```

## 🎯 Next Steps

1. **Verify domain availability** ✓
2. **Register akudemy.com** (Namecheap, GoDaddy)
3. **Push to GitHub** 
4. **Deploy to Vercel**
5. **Configure custom domain**
6. **Test site** (all pages load, links work)

## ✅ Pre-Launch Checklist

- [ ] All HTML files created
- [ ] Navigation links tested
- [ ] Mobile responsive tested
- [ ] Domain registered
- [ ] GitHub repository created
- [ ] Vercel project deployed
- [ ] Custom domain configured
- [ ] SSL certificate active
- [ ] All pages accessible
- [ ] Links working (no 404s)
- [ ] Social media preview tested (OpenGraph)

## 📞 Support

**Vercel Support**: vercel.com/support  
**Netlify Support**: netlify.com/support

