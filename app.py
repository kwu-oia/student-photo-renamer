#!/usr/bin/env python3
"""
Simple Streamlit UI: upload validation Excel + images, run rename-by-validation.
"""

import io
import shutil
import tempfile
from pathlib import Path

import openpyxl
import streamlit as st

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def load_passed_mapping_from_bytes(data: bytes) -> dict:
    """Load validation Excel from bytes; return dict 수험번호 -> 학번."""
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    ws = wb.active
    mapping = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or row[0] is None:
            continue
        hakbeon, suheom = row[0], row[1]
        if suheom is not None:
            key = str(int(suheom) if isinstance(suheom, (int, float)) else suheom).strip()
            val = str(int(hakbeon) if isinstance(hakbeon, (int, float)) else hakbeon).strip()
            mapping[key] = val
    wb.close()
    return mapping


def run_rename(excel_bytes: bytes, image_dir: Path, out_dir: Path) -> list[str]:
    """Process images; copy renamed files to out_dir. Return log lines."""
    passed = load_passed_mapping_from_bytes(excel_bytes)
    log = []
    log.append(f"Loaded {len(passed)} passed students from validation file.")
    log.append(f"Output folder: {out_dir}")

    out_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped = 0
    for f in image_dir.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() not in IMAGE_EXTENSIONS:
            continue
        suheom = f.stem
        if suheom in passed:
            hakbeon = passed[suheom]
            dest = out_dir / f"{hakbeon}{f.suffix}"
            if dest.exists():
                log.append(f"Skip (exists): {f.name} -> {dest.name}")
                continue
            shutil.copy2(f, dest)
            copied += 1
            log.append(f"Copied: {f.name} -> {dest.name}")
        else:
            skipped += 1
            log.append(f"Skipped (not passed): {f.name}")

    log.append("")
    log.append(f"Done. Copied: {copied}, Skipped: {skipped}")
    return log


st.set_page_config(page_title="Photo renamer tool", layout="centered")
st.title("Photo renamer tool")

with st.expander("📖 User guide — What this does and how to use it", expanded=True):
    st.markdown("""
    **What it does**  
    This tool takes student photos named by **수험번호** (exam/application number) and produces a set of photos named by **학번** (student ID) for **passed students only**.  
    - Only students listed in your validation file are included.  
    - Each photo is renamed from 수험번호 (e.g. `11002.jpg`) to the matching 학번 (e.g. `2025509514.jpg`).  
    - Your original files are never changed; you download the result as a ZIP.

    **What you need**  
    1. **Validation Excel** — One `.xlsx` or `.xls` file with two columns: **학번** (student ID) and **수험번호** (exam number). Only include rows for students who **passed**.  
    2. **Image files** — Photos named by 수험번호 (e.g. `11001.jpg`, `11002.png`). You can select multiple files or drop a folder’s worth.

    **How to use it**  
    1. Upload your validation Excel file in the first box.  
    2. Upload or drop all image files in the second box.  
    3. Click **Rename files**.  
    4. When it’s done, check the log and click **Save as…** to save the renamed images as a ZIP to your computer.
    """)

excel_file = st.file_uploader("Validation Excel file", type=["xlsx", "xls"], key="excel")
if not excel_file:
    st.info("Upload a validation Excel file (columns: 학번, 수험번호).")

image_files = st.file_uploader(
    "Image files (select multiple or drop folder contents)",
    type=["jpg", "jpeg", "png", "gif", "webp"],
    accept_multiple_files=True,
    key="images",
)
if not image_files:
    st.info("Upload one or more image files (filenames = 수험번호).")

if excel_file and image_files:
    if st.button("Rename files"):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "images"
            src.mkdir()
            for f in image_files:
                path = src / (f.name or f"image_{id(f)}")
                path.write_bytes(f.getvalue())
            out = Path(tmp) / "renamed"
            excel_bytes = excel_file.getvalue()
            with st.spinner("Processing…"):
                log_lines = run_rename(excel_bytes, src, out)

            st.subheader("Log")
            log_text = "\n".join(log_lines)
            st.text_area("Log output", value=log_text, height=300, disabled=True, label_visibility="collapsed")

            # Offer zip of output folder
            if (out).exists() and any(out.iterdir()):
                import zipfile
                zip_path = Path(tmp) / "output.zip"
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for f in out.rglob("*"):
                        if f.is_file():
                            zf.write(f, f.relative_to(out))
                st.success("Completed. Save the renamed images below.")
                st.download_button(
                    "Download",
                    data=zip_path.read_bytes(),
                    file_name="renamed_images.zip",
                    mime="application/zip",
                )
