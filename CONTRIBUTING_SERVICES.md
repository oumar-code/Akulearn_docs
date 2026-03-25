# Contribution Guidelines for All Aku Platform Services

Thank you for your interest in contributing to the Aku platform! Please follow these guidelines for all service repositories (Telhone, IGHub, SuperHub, AkuWorkspace, DaaS, AkuAI, AkuTutor, etc.).

## Getting Started

- Fork the repository and clone your fork locally.
- Create a new feature branch for your changes.
- Keep commits focused and atomic.
- Write clear, descriptive commit messages.


## Code Style & Quality

- Follow the code style and linting rules for each service.
- Write and run tests for your changes.
- Ensure your code passes CI before submitting a PR.


## Environment Variables

- Never commit secrets or `.env` files. See `ENVIRONMENT.md` for details.


## Opening a Pull Request

- Sync with the latest `main` branch before pushing.
- Open a Pull Request against `main`.
- Fill out the PR template (if available) and describe your changes.


## What NOT to Commit

- Secrets, `.env` files, or credentials
- Build artifacts or dependencies (e.g., `node_modules/`, `site/`)
- IDE/editor config files not required by the project


## Questions

Open an issue or discussion in the relevant repository if you have questions.
