# Usage Guide

This guide provides step-by-step instructions on how to use and customize the Automated Resume Builder to create, compile, and deploy your professional resume.

---

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Local Setup](#2-local-setup)
3. [Customizing Your Data (`data.yaml`)](#3-customizing-your-data-datayaml)
4. [Customizing the PDF Template (`template.tex`)](#4-customizing-the-pdf-template-templatetex)
5. [Local Compilation](#5-local-compilation)
6. [GitHub Actions CI/CD Deployment](#6-github-actions-cicd-deployment)
7. [Dockerized Local Build](#7-dockerized-local-build)

---

## 1. Prerequisites

You can compile the resume either locally using Python & LaTeX, or in an isolated Docker container.

### For Local Compilation (Recommended for rapid editing):
- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv)**: A fast Python package installer and resolver.
- **TeX Live** (or MacTeX/MikTeX) containing `pdflatex`.

### For Dockerized Compilation:
- **Docker** installed and running on your system.

---

## 2. Local Setup

1. **Clone your repository** (or your fork):
   ```bash
   git clone https://github.com/yourusername/latest-resume.git
   cd latest-resume
   ```

2. **Install Python dependencies** using `uv`:
   ```bash
   uv sync
   ```
   This command creates a virtual environment (`.venv`) and installs the exact versions of dependencies from `uv.lock` (such as Jinja2, PyYAML, and Ruff).

---

## 3. Customizing Your Data (`data.yaml`)

Resume content is entirely separated from presentation and resides in `src/data.yaml`. Open this file and replace the placeholders with your actual information:

### Key Sections to Update:
* **personal**: 
  - `name`: Your full name.
  - `email`: Your email address.
  - `phone_display` & `phone_href`: Your contact number.
  - `website`, `linkedin`, `github`: URLs and display text for your portfolios.
* **education**: Institution, degree, dates, GPA, and coursework list.
* **experience**: A list of jobs containing title, company, dates, and bulleted highlights.
* **projects**: GitHub URLs, descriptions, highlights, and tools used.
* **technologies**: Grouped skills (e.g. Languages, ML, Tools) and specific entries.
* **courses**: Online certificates or intensive training with URLs.
* **honors**: Competitions, hackathons, and certifications.
* **extracurricular**: Voluntary work or student activities.

> [!WARNING]
> **Jinja2 Keyword Conflicts**: Avoid using reserved Python dictionary method names as top-level keys or list keys in YAML (such as `items`, `keys`, `values`, `get`, `update`, `pop`). If you need to list items, name the key `tools`, `highlights`, or something custom.

---

## 4. Customizing the PDF Template (`template.tex`)

The visual layout of the PDF is managed inside `src/template.tex` using standard LaTeX alongside Jinja2 templates.

To avoid syntax conflicts with LaTeX's heavy use of curly braces `{ }`, we use custom Jinja delimiters:

| Delimiter Syntax | Jinja Purpose | Example |
|---|---|---|
| `<< variable >>` | Variable Rendering | `<< personal.name >>` |
| `<% for ... %>` / `<% endfor %>` | Loops | `<% for job in experience %>` |
| `<% if ... %>` / `<% endif %>` | Conditionals | `<% if course.institution %>` |
| `<# comment #>` | Comments | `<# This is ignored #>` |

### Customizing Styles:
- **Margins & Page Limits**: Modify the `geometry` package options at the top of the file to fit your resume onto a single page or two pages.
- **Colors**: Adjust `primaryColor` and `linkColor` RGB values to fit your brand.
- **Section Headers**: Tweak `\titleformat` and `\titlespacing` to manage vertical spacing.

---

## 5. Local Compilation

To compile your resume locally into a PDF:

```bash
uv run src/build.py
```

### What this script does:
1. Loads and validates `src/data.yaml`.
2. Compiles `src/template.tex` with Jinja2 to produce a raw LaTeX file `generated.tex` at the project root.
3. Invokes `pdflatex` on `generated.tex`.
4. Outputs the final `resume.pdf` to the project root.
5. Cleans up intermediate build files (like `.aux`, `.log`).

---

## 6. GitHub Actions CI/CD Deployment

Every commit pushed to the `main` branch triggers an automated build that generates your PDF and deploys a landing page to GitHub Pages.

### Setup Instructions for Your Fork:
1. Go to your repository on GitHub.
2. Navigate to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, select **GitHub Actions**.
4. Push a commit to `main`. The `Build and Deploy Resume` workflow will trigger automatically.
5. Once complete, your live site will be available at:
   `https://<yourusername>.github.io/<repository-name>/`
   which serves `src/index.html` and hosts the compiled `resume.pdf`.

---

## 7. Dockerized Local Build

If you don't have LaTeX installed locally, you can use the provided Docker container to compile your PDF using the same environment as the CI/CD pipeline:

1. **Build the Docker builder image**:
   ```bash
   docker build -t resume-builder .
   ```

2. **Compile the resume inside the container**:
   ```bash
   docker run --rm -v "$(pwd):/workspace" -w /workspace resume-builder sh -lc "uv sync --frozen && uv run src/build.py"
   ```
   This mounts your workspace, runs the dependency synchronization, and outputs the compiled `resume.pdf` directly to your local project root.
