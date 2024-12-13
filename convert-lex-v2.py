import json
import re
from datetime import datetime
import random
import string
import sys
import os

def generate_id(length=8):
    """Generate a random ID similar to the ones in the JSON file."""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def get_timestamp():
    """Get current timestamp in the format DD.MM.YYYY - HH:mm"""
    now = datetime.now()
    return now.strftime("%d.%m.%Y - %H:%M")

def convert_md_to_json(md_file_path):
    # Generate output path by replacing .md extension with .json
    json_file_path = os.path.splitext(md_file_path)[0] + '.json'

    # Read markdown file
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{md_file_path}' not found")
        sys.exit(1)

    # Regular expression to match sections
    section_pattern = r'## "([^"]+)"\s*(?:<!-- start-section-[a-z0-9]+ -->)\s*([\s\S]*?)(?:<!-- end-section-[a-z0-9]+ -->)'
    
    sections = []
    for match in re.finditer(section_pattern, content):
        title = match.group(1)
        content = match.group(2).strip()

        # Clean up content
        content = re.sub(r'^is no code provided.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^asdasd$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^vided does not contain.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^-->$', '', content, flags=re.MULTILINE)
        content = content.strip()

        if content:  # Only add non-empty sections
            sections.append({
                "id": generate_id(),
                "title": title,
                "content": content,
                "timestamp": get_timestamp()
            })

    # Create final JSON structure
    json_output = {
        "version": "1.0",
        "sections": sections
    }

    # Write to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(json_output, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion completed. Output saved to: {json_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert.py <input-markdown-file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    convert_md_to_json(input_file)
