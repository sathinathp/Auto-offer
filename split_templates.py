import os
import re

def split_template(src_html_path, dest_html_path, dest_css_path):
    with open(src_html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the style block
    style_pattern = re.compile(r'<style>(.*?)</style>', re.DOTALL)
    match = style_pattern.search(content)
    
    if not match:
        print(f"No style block found in {src_html_path}")
        return

    css_content = match.group(1).strip()
    
    # We want to extract the main CSS but leave the {% if preview_mode %} blocks in the HTML
    # Let's find any conditional preview_mode CSS block in css_content
    # e.g., {% if preview_mode %} ... {% endif %} or {% else %} ... {% endif %}
    # We can keep the whole CSS in the css file, and just remove the jinja tags or handle them.
    # Actually, Weasyprint doesn't process Jinja inside static files.
    # So we should put all non-preview_mode styles into the static CSS file,
    # and leave the preview_mode styles in the HTML.
    
    # Let's extract the preview_mode styles
    preview_style_pattern = re.compile(r'({%\s*if\s+preview_mode\s*%}.*?{%\s*endif\s*%})', re.DOTALL)
    preview_match = preview_style_pattern.search(css_content)
    
    preview_css = ""
    clean_css = css_content
    if preview_match:
        preview_css = preview_match.group(1).strip()
        # Remove it from clean_css
        clean_css = preview_style_pattern.sub('', clean_css).strip()

    # Write CSS file
    os.makedirs(os.path.dirname(dest_css_path), exist_ok=True)
    with open(dest_css_path, 'w', encoding='utf-8') as f:
        f.write(clean_css)
    print(f"Created CSS: {dest_css_path}")

    # Replace <style>...</style> in HTML with link to CSS and the preview_css
    link_tag = f'<link rel="stylesheet" href="/static/css/{os.path.basename(dest_css_path)}">'
    if preview_css:
        replacement = f'{link_tag}\n<style>\n{preview_css}\n</style>'
    else:
        replacement = link_tag

    new_html_content = style_pattern.sub(replacement, content)
    
    os.makedirs(os.path.dirname(dest_html_path), exist_ok=True)
    with open(dest_html_path, 'w', encoding='utf-8') as f:
        f.write(new_html_content)
    print(f"Created HTML: {dest_html_path}")

if __name__ == "__main__":
    split_template(
        "templates/offer_letter_template.html",
        "templates/offer_letters/bluebix_offer.html",
        "static/css/bluebix_offer.css"
    )
    split_template(
        "templates/petabytz_template.html",
        "templates/offer_letters/petabytz_offer.html",
        "static/css/petabytz_offer.css"
    )
