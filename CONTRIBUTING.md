# Contributing to ProcessPilot

Thank you for considering contributing to ProcessPilot! Here are some guidelines to help you get started:

---

## How to Contribute

1. Fork the repository.
2. Clone your fork:
   ```sh
   git clone https://github.com/your-username/ProcessPilot.git
   ```
3. Create a new branch for your feature or bug fix:
   ```sh
   git checkout -b feature-name
   ```
4. Make your changes and commit them:
   ```sh
   git commit -m "Add feature-name"
   ```
5. Push your branch to your fork:
   ```sh
   git push origin feature-name
   ```
6. Open a pull request on the main repository.

---

## Code Style Guidelines

### Backend (Python)

- Follow **PEP 8** for Python code.
- Use meaningful variable and function names.
- Add docstrings to functions and classes for clarity.
- Use type hints where applicable.

### Frontend (React/JavaScript)

- Use **ESLint** and **Prettier** for consistent formatting.
- Follow React best practices (e.g., functional components, hooks).
- Keep components modular and reusable.
- Use descriptive prop names and default props where necessary.

---

## Testing

### Backend

- Write unit tests for all new features or bug fixes.
- Place test files in the `backend/tests` directory.
- Run tests before submitting your pull request:
  ```sh
  python -m unittest discover backend/tests
  ```

### Frontend

- Write tests for React components using **Jest** and **React Testing Library**.
- Place test files in the `frontend/src/tests` directory.
- Run tests before submitting your pull request:
  ```sh
  npm test
  ```

---

## Reporting Issues

If you find a bug or have a feature request, please open an issue with the following details:

- **Steps to reproduce the issue** (if applicable).
- **Expected behavior**.
- **Actual behavior**.
- **Screenshots or logs** (if applicable).

---

## Pull Request Guidelines

1. Ensure your branch is up to date with the `main` branch:
   ```sh
   git fetch origin
   git checkout main
   git merge origin/main
   ```
2. Resolve any merge conflicts before submitting your pull request.
3. Include a clear and descriptive title for your pull request.
4. Provide a detailed description of the changes you made.
5. Ensure all tests pass before submitting your pull request.

---

## Security Guidelines

- Validate all user inputs to prevent security vulnerabilities.
- Avoid hardcoding sensitive information (e.g., API keys).
- Use environment variables for sensitive data.
- Review dependencies for known vulnerabilities.

---

## Community Guidelines

- Be respectful and inclusive in all interactions.
- Provide constructive feedback during code reviews.
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md) (if applicable).

---

Thank you for contributing to ProcessPilot! Your efforts help make this project better for everyone.
