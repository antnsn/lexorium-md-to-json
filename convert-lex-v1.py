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

def extract_section_title(content):
    """Extract the title from the section content."""
    title_match = re.search(r'^## (.+?)\s*$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1)
    return None

def clean_content(content):
    """Clean up the content by removing the title line and extra whitespace."""
    # Remove the title line
    content = re.sub(r'^## .+?\s*$', '', content, flags=re.MULTILINE)
    # Remove empty lines from start and end
    content = content.strip()
    return content

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
    # This pattern matches content between start-section and end-section tags
    section_pattern = r'<!-- start-section-[^>]+ -->\s*(.*?)\s*<!-- end-section-[^>]+ -->'
    
    # Dictionary to store latest version of each section by title
    sections_dict = {}
    
    for match in re.finditer(section_pattern, content, re.DOTALL):
        section_content = match.group(1).strip()
        
        # Extract title and clean content
        title = extract_section_title(section_content)
        if title:
            cleaned_content = clean_content(section_content)
            if cleaned_content:  # Only add non-empty sections
                # Update or add the section with latest content
                sections_dict[title] = {
                    "id": generate_id(),
                    "title": title,
                    "content": cleaned_content,
                    "timestamp": get_timestamp()
                }

    # Convert dictionary values to list
    sections = list(sections_dict.values())

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
        print("Usage: python convert_quick_notes.py <input-markdown-file>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    convert_md_to_json(input_file)
