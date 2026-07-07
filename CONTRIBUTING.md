# Contributing to Automated Resume Builder

Thank you for your interest in contributing! Whether you are seeking to fork this repository to build your own custom resume, extend the features of the build script, or contribute templates and fixes back upstream, we welcome your involvement.

---

## Forking & Creating Your Personal Resume

This project is designed to be highly forkable. If you want to use this builder to maintain your own resume, follow these steps:

1. **Fork the Repository**:
   Click the **Fork** button at the top right of this repository's GitHub page.

2. **Clone Your Fork**:
   ```bash
   git clone https://github.com/yourusername/latest-resume-for-public.git
   cd latest-resume-for-public
   ```

3. **Anonymization & Initial Config**:
   By default, `src/data.yaml` contains masked/placeholder contact fields. Keep this as-is if you plan to keep your repository public but want to avoid scraping of your phone number and personal email. You can configure a separate private branch or git-ignored configuration if you want to swap out files before building, or compile locally.

4. **GitHub Actions Activation**:
   Ensure you enable GitHub Actions in your fork settings and configure GitHub Pages to build from **GitHub Actions** under **Settings > Pages** so your resume deploys automatically on every push.

5. **Continuing Development**:
   Feel free to add custom packages in the `Dockerfile` or modify `src/build.py` to adapt the compilation to your needs.

---

## Modifying the Build System & Code base

If you plan to contribute improvements back to this repository, please adhere to the following development guidelines:

### Development Workflow

1. **Install Dependencies**:
   Ensure you have [uv](https://github.com/astral-sh/uv) installed, then sync the virtual environment:
   ```bash
   uv sync
   ```

2. **Linting and Formatting**:
   We use **Ruff** for code analysis and formatting. Before submitting changes, run Ruff to ensure everything complies with coding standards:
   ```bash
   # Check lint rules
   uv run ruff check .
   
   # Automatically format code
   uv run ruff format .
   ```

3. **Validating PDF Build Output**:
   Any change made to `src/build.py`, `src/template.tex`, or `src/data.yaml` must not break the compilation. Ensure the following command runs successfully and generates a valid PDF:
   ```bash
   uv run src/build.py
   ```

4. **Docker Testing**:
   Ensure your changes compile successfully inside the Docker container to prevent CI/CD failures:
   ```bash
   docker build -t resume-builder-test .
   docker run --rm -v "$(pwd):/workspace" -w /workspace resume-builder-test sh -lc "uv sync --frozen && uv run src/build.py"
   ```

### Code Style Guidelines

- **Separate Data & Presentation**:
  - Do not add hardcoded content in `src/template.tex` or `src/build.py`. All resume-related details must come from `src/data.yaml`.
  - Avoid inline formatting (like direct LaTeX commands) inside `src/data.yaml` where possible, keeping it purely structured data.
- **Python Code**:
  - Follow PEP 8 guidelines.
  - Keep functions focused and write clear error messages.
- **LaTeX Templates**:
  - Keep custom packages to a minimum in `src/template.tex` unless necessary.
  - Document any new packages added so they can be included in the base `Dockerfile`.

### Submitting a Pull Request (PR)

1. Commit your changes with descriptive messages:
   ```bash
   git commit -m "feat: add schema validation for data.yaml using pydantic"
   ```
2. Push to your fork:
   ```bash
   git push origin branch-name
   ```
3. Open a Pull Request on GitHub against the `main` branch of the original repository.
4. Describe the changes, why they are needed, and confirm that all local tests (compilation and formatting) pass successfully.
