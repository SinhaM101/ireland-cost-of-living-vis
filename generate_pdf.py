import markdown
from weasyprint import HTML, CSS

with open('DESIGN_DOCUMENT.md', 'r') as f:
    md_content = f.read()

html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            color: #333;
        }}
        h1 {{
            font-size: 20pt;
            color: #1a5f2a;
            border-bottom: 2px solid #1a5f2a;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            font-size: 14pt;
            color: #2d7a3e;
            margin-top: 25px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        h3 {{
            font-size: 12pt;
            color: #444;
            margin-top: 20px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f5f5f5;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
            font-size: 10pt;
        }}
        em {{
            color: #666;
        }}
        strong {{
            color: #222;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 25px 0;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        p {{
            margin: 10px 0;
        }}
        @page {{
            size: A4;
            margin: 2cm;
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

HTML(string=full_html).write_pdf('DESIGN_DOCUMENT.pdf')
print("PDF generated: DESIGN_DOCUMENT.pdf")
