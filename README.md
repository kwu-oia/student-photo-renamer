# 📖 Student Photo Renamer — User Guide

**An internal tool for Kwangwoon University International Office**

This guide explains how to use the Student Photo Renamer web tool to convert student photo filenames from exam/application numbers (**수험번호**) to student IDs (**학번**) for **passed students only**. You can use it directly here:

**Live demo:** https://kwuimgrename.streamlit.app/

> 💡 **Why this tool?** While it's a simple script, it saves countless hours of manual file renaming work. Instead of renaming hundreds of student photos one by one, this tool processes them all in seconds with automatic validation against your passed student list. Perfect for streamlining international office workflows!

---

## What the tool does

This tool takes student photos named by **수험번호** (exam/application number) and produces a set of photos named by **학번** (student ID) **only for passed students**.

![Data Flow Diagram](/Users/universe/.cursor/projects/Users-universe-Projects-student-photo-renamer/assets/data-flow-diagram.png)

Key features:
- ✅ Only students listed in your **validation Excel file** are included
- ✅ Each photo is renamed from 수험번호 to matching 학번 (e.g., `11002.jpg` → `2025509514.jpg`)
- ✅ Your original files are never changed
- ✅ Download results as a convenient **ZIP** file

---

## What you need

You need **two types of input**:

### 1️⃣ Validation Excel file

```
File format: .xlsx or .xls

┌────────────┬────────────┐
│   학번     │ 수험번호   │
├────────────┼────────────┤
│ 2025509512 │   11001    │
│ 2025509514 │   11002    │
│ 2025509515 │   11005    │
│ 2025509520 │   11010    │
└────────────┴────────────┘

Requirements:
• Two columns: 학번 and 수험번호
• Include ONLY students who passed
• File can be .xlsx or .xls format
```

### 2️⃣ Image files

```
Photo filenames (based on 수험번호):

📁 Your folder
  ├── 11001.jpg
  ├── 11002.png
  ├── 11003.jpg
  ├── 11005.jpg
  └── 11010.jpg

✓ Supported formats: jpg, png, gif, etc.
✓ Can upload multiple files at once
✓ Can drag and drop entire folder contents
```

---

## How to use the tool

### 📋 Step-by-step workflow

![Workflow Diagram](/Users/universe/.cursor/projects/Users-universe-Projects-student-photo-renamer/assets/workflow-diagram.png)

### Detailed steps:

**1. Upload the validation Excel file**
   - Click the **"Validation Excel file"** uploader
   - Select your `.xlsx` or `.xls` file with columns **학번** and **수험번호**
   - File is loaded and stored in memory

**2. Upload the image files**
   - Click the **"Image files"** uploader
   - Select multiple photos OR drag a whole folder into the uploader
   - All files with 수험번호 filenames are accepted

**3. Run the renaming process**
   - Click the **"Rename files"** button
   - Processing begins (a spinner shows while it works)
   - The tool matches each photo's filename against your validation list

**4. Review the processing log**
   - After processing, a **Log** section appears showing:
   
   ```
   ✓ Loaded 1,500 passed students
   
   📝 Processing details:
   ├── ✅ 11001.jpg → 2025509512.jpg (copied)
   ├── ✅ 11002.jpg → 2025509514.jpg (copied)
   ├── ⏭️  11004.jpg (skipped - not in validation file)
   ├── ✅ 11005.jpg → 2025509515.jpg (copied)
   └── ...
   
   📊 Summary: 1,497 copied, 3 skipped
   ```

**5. Download your renamed photos**
   - When complete, click the **"Download"** button
   - Saves as `renamed_images.zip` to your computer
   - ZIP contains all renamed images organized by 학번

---

## Example walkthrough

![Transformation Diagram](/Users/universe/.cursor/projects/Users-universe-Projects-student-photo-renamer/assets/transformation-diagram.png)
