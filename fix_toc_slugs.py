import glob, re, os

def gfm_slugify(text):
    # GitHub Flavored Markdown slugify:
    # 1. Lowercase
    # 2. Strip punctuation/symbols [^\w\s-] (keeps spaces, letters, digits, _, -)
    # 3. Replace each space with a dash '-'
    s = text.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = s.replace(' ', '-')
    return s

for doc in glob.glob("docs/*.md"):
    with open(doc, "r", encoding="utf-8") as f:
        lines = f.readlines()

    headings = []
    for line in lines:
        m = re.match(r'^##\s+(.*)', line.strip())
        if m:
            h_text = m.group(1).strip()
            if "Table of Contents" not in h_text and "📑" not in h_text:
                clean_title = re.sub(r'^[0-9]+\.\s*', '', h_text).strip()
                clean_title = re.sub(r'^[^\w\d]+', '', clean_title).strip()
                slug = gfm_slugify(h_text)
                headings.append((clean_title, slug))

    new_lines = []
    in_toc = False
    for line in lines:
        if "## 📑 Table of Contents" in line or "## Table of Contents" in line:
            new_lines.append("## 📑 Table of Contents\n\n")
            for idx, (title, slug) in enumerate(headings, 1):
                new_lines.append(f"{idx}. [{title}](#{slug})\n")
            new_lines.append("\n")
            in_toc = True
            continue

        if in_toc:
            if line.strip().startswith("---") or (line.strip().startswith("## ") and "Table of Contents" not in line):
                in_toc = False
                new_lines.append(line)
            continue

        new_lines.append(line)

    with open(doc, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

print("GFM slugs aligned!")
