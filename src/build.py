import sys
import subprocess
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader


SRC_DIR = Path(__file__).parent
PROJECT_ROOT = SRC_DIR.parent
DATA_FILE = SRC_DIR / "data.yaml"
TEMPLATE_FILE = "template.tex"
GENERATED_TEX = Path("generated.tex")
OUTPUT_PDF = PROJECT_ROOT / "resume.pdf"

REQUIRED_TOP_LEVEL_KEYS = [
    "personal",
    "education",
    "experience",
    "projects",
    "technologies",
    "courses",
    "honors",
    "extracurricular",
]


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def validate(data: dict) -> None:
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in data]
    if missing:
        raise ValueError(f"data.yaml is missing required keys: {missing}")


def build_jinja_environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(SRC_DIR)),
        variable_start_string="<<",
        variable_end_string=">>",
        block_start_string="<%",
        block_end_string="%>",
        comment_start_string="<#",
        comment_end_string="#>",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
    )


def render(data: dict) -> str:
    env = build_jinja_environment()
    template = env.get_template(TEMPLATE_FILE)
    return template.render(**data)


def write_tex(content: str) -> None:
    GENERATED_TEX.write_text(content)


def run_pdflatex() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", str(GENERATED_TEX)],
        capture_output=True,
        text=True,
    )


def abort_with_log(result: subprocess.CompletedProcess) -> None:
    print("Build failed. pdflatex output:", file=sys.stderr)
    print(result.stdout[-4000:], file=sys.stderr)
    sys.exit(1)


def publish_pdf() -> None:
    generated_pdf = GENERATED_TEX.with_suffix(".pdf")
    generated_pdf.rename(OUTPUT_PDF)


def main() -> None:
    data = load_yaml(DATA_FILE)
    validate(data)
    tex_content = render(data)
    write_tex(tex_content)
    result = run_pdflatex()
    if result.returncode != 0:
        abort_with_log(result)
    publish_pdf()
    print(f"Build successful → {OUTPUT_PDF}")
    print("cleaning up...")
    # GENERATED_TEX.unlink(missing_ok=True)
    (GENERATED_TEX.with_suffix(".aux")).unlink(missing_ok=True)
    (GENERATED_TEX.with_suffix(".log")).unlink(missing_ok=True)
    print("done.")


if __name__ == "__main__":
    main()
