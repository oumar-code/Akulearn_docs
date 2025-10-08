#!/bin/bash
# Deploy Aku Admin Portal Frontend (Vue.js)

npm install
npm run build
# Copy dist/ to your web server directory
cp -r dist/* /var/www/html/admin/
echo "Admin portal frontend deployed to /var/www/html/admin/"
