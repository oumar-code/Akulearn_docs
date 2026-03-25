# Environment Variables and Secrets Management

Each service in the Aku platform uses environment variables for configuration and secrets. **Never commit secrets or sensitive values to the repository.**

## How to Use Environment Variables

1. **Create a `.env` file** in the root of each service (e.g., `Telhone/.env`, `IGHub/.env`).
2. Add your environment variables in the format:
   ```env
   # Example
   NODE_ENV=development
   API_KEY=your-api-key-here
   DB_URL=your-database-url
   ```
3. **Do not commit `.env` files.** They are excluded by `.gitignore`.
4. For production, set environment variables securely in your deployment platform (e.g., Vercel, AWS, GCP, Azure).

## Best Practices
- Use different `.env` files for development, testing, and production.
- Rotate secrets regularly.
- Never log secrets or print them in error messages.

## References
- [12 Factor App: Config](https://12factor.net/config)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
