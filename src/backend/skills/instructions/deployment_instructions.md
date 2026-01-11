# Deployment Instructions

## Skill: Deployment Orchestrator

### Objective
Safely and efficiently deploy backend services, frontend applications, and educational content to production environments with proper validation and rollback capabilities.

### Deployment Types

#### 1. Backend Deployment
- Deploy FastAPI services
- Update database schemas
- Deploy API endpoints
- Update authentication services
- Deploy background workers

#### 2. Frontend Deployment
- Deploy React/Next.js applications
- Update static assets
- Deploy PWA components
- Update service workers

#### 3. Content Deployment
- Deploy educational content batches
- Update curriculum data
- Deploy multimedia assets
- Update search indices

#### 4. Database Migrations
- Execute schema migrations
- Update seed data
- Optimize indices
- Update constraints

### Pre-Deployment Checklist

#### Critical Checks
- [ ] All tests pass (unit, integration, e2e)
- [ ] Code review completed and approved
- [ ] Content validation passed
- [ ] Database backups are recent
- [ ] Rollback plan is documented
- [ ] Environment variables are configured
- [ ] Dependencies are up to date
- [ ] Security scan completed

#### Infrastructure Checks
- [ ] Server resources are adequate
- [ ] Database connections are available
- [ ] Storage space is sufficient
- [ ] Network connectivity is stable
- [ ] Load balancer is configured
- [ ] SSL certificates are valid

#### Content Deployment Checks
- [ ] Content validation passed
- [ ] Asset files are uploaded
- [ ] Metadata is complete
- [ ] Search index is ready
- [ ] Cache invalidation planned

### Deployment Process

#### Phase 1: Preparation (5-10 min)
1. Create deployment branch
2. Run all tests
3. Build production artifacts
4. Verify environment configuration
5. Create database backup
6. Document deployment plan

#### Phase 2: Pre-Deployment (2-5 min)
1. Put application in maintenance mode (if needed)
2. Stop background workers
3. Clear caches
4. Verify database connectivity
5. Check resource availability

#### Phase 3: Deployment (10-30 min)
1. Deploy database migrations (if any)
2. Deploy backend services
3. Deploy frontend application
4. Deploy content updates
5. Update configuration
6. Restart services

#### Phase 4: Verification (5-15 min)
1. Health check all endpoints
2. Verify database connections
3. Test critical user flows
4. Check content availability
5. Monitor error logs
6. Verify performance metrics

#### Phase 5: Post-Deployment (5-10 min)
1. Remove maintenance mode
2. Clear CDN caches
3. Update monitoring dashboards
4. Notify team of completion
5. Document any issues
6. Archive deployment logs

### Rollback Procedures

#### When to Rollback
- Critical errors in production
- Data integrity issues
- Performance degradation > 50%
- Security vulnerabilities discovered
- Multiple user-facing errors

#### Rollback Steps
1. Activate rollback plan
2. Restore previous version
3. Restore database backup (if needed)
4. Clear caches
5. Verify system stability
6. Document rollback reason
7. Schedule fix deployment

### Environment-Specific Guidelines

#### Development Environment
- Deploy frequently
- Skip some validation steps
- Use development database
- Enable debug logging
- No rollback plan needed

#### Staging Environment
- Full deployment process
- Complete testing required
- Use staging database
- Monitor closely
- Test rollback procedures

#### Production Environment
- Strict validation required
- Full testing and approval
- Production database
- Minimal downtime
- Rollback plan mandatory
- User communication required

### Deployment Strategies

#### 1. Blue-Green Deployment
- Deploy to inactive environment
- Verify functionality
- Switch traffic to new environment
- Keep old environment as backup

#### 2. Rolling Deployment
- Deploy to servers gradually
- Monitor each batch
- Continue if successful
- Rollback specific servers if needed

#### 3. Canary Deployment
- Deploy to small user subset
- Monitor metrics carefully
- Gradually increase traffic
- Full rollout if successful

### Monitoring Requirements

#### During Deployment
- Error rates
- Response times
- Database connections
- Memory usage
- CPU usage
- Disk space

#### Post-Deployment (First Hour)
- Application errors
- API response times
- Database query performance
- User session counts
- Content load times
- Search functionality

#### Extended Monitoring (24 Hours)
- User engagement metrics
- Content access patterns
- API usage patterns
- Database performance
- Cache hit rates
- Error trends

### Communication Protocol

#### Before Deployment
- Notify team of deployment window
- Update status page
- Send user notifications (if needed)

#### During Deployment
- Post updates in team chat
- Update deployment status
- Report any issues immediately

#### After Deployment
- Confirm deployment success
- Share deployment summary
- Document lessons learned
- Update deployment logs

### Best Practices

1. **Always Test First**: Deploy to staging before production
2. **Automate Everything**: Use scripts and CI/CD pipelines
3. **Monitor Closely**: Watch metrics during and after deployment
4. **Have a Rollback Plan**: Always be ready to revert
5. **Deploy in Low-Traffic Periods**: Minimize user impact
6. **Backup Everything**: Database, code, configuration
7. **Document Everything**: Keep detailed deployment logs
8. **Communicate Clearly**: Keep team and users informed

### Security Considerations

- Verify SSL certificates before deployment
- Rotate secrets and API keys
- Update security headers
- Check for exposed credentials
- Validate authentication flows
- Test authorization rules
- Verify CORS configuration
- Check rate limiting

### Performance Optimization

- Enable gzip compression
- Optimize static asset delivery
- Configure CDN properly
- Set appropriate cache headers
- Optimize database queries
- Index database tables
- Configure connection pooling
- Set reasonable timeouts

### Troubleshooting Common Issues

#### Deployment Fails
1. Check deployment logs
2. Verify environment variables
3. Test database connectivity
4. Check resource availability
5. Verify dependencies are installed

#### Application Won't Start
1. Check application logs
2. Verify configuration files
3. Test database connection
4. Check port availability
5. Verify file permissions

#### Content Not Appearing
1. Verify content deployment completed
2. Check database records
3. Clear caches
4. Verify file uploads
5. Check search indexing

#### Performance Degradation
1. Check server resources
2. Review database queries
3. Verify cache configuration
4. Check external API calls
5. Review recent code changes
