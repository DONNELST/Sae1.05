import markdown

with open("analyse_tcpdump.md", "r", encoding="utf-8") as f:
    md_text = f.read()

html = markdown.markdown(md_text, extensions=["tables"])

with open("analyse_tcpdump.html", "w", encoding="utf-8") as f:
    f.write(html)

