# Lexorium MD to JSON Converter

A Python-based tool for converting Lexorium-formatted Markdown files to JSON format. This repository contains two converters:
- `convert-lex-v1.py`: Converts Markdown files from Lexorium v1.x.x format
- `convert-lex-v2.py`: Converts Markdown files from Lexorium v2.x.x format

## Features

- Converts Lexorium-style Markdown sections to JSON
- Maintains code blocks and formatting
- Handles section markers (`<!-- start-section-[name] -->` and `<!-- end-section-[name] -->`)
- Generates unique IDs for each section
- Adds timestamps to each section
- Prevents duplicate sections by keeping only the latest version
- Preserves the original content structure
- Supports both Lexorium v1.x.x and v2.x.x formats

## Usage

For Lexorium v1.x.x files:
```bash
python3 convert-lex-v1.py <input-markdown-file>
```

For Lexorium v2.x.x files:
```bash
python3 convert-lex-v2.py <input-markdown-file>
```

The script will generate a JSON file in the same location as your input file, with the same name but a `.json` extension.

### Example

If you have a file named `quick-notes.md` in Lexorium v1 format:
```bash
python3 convert-lex-v1.py quick-notes.md
```

For a file in Lexorium v2 format:
```bash
python3 convert-lex-v2.py testv2.md
```

Both commands will create corresponding `.json` files in the same directory.

## Input Format

### Lexorium v1.x.x Format
```markdown
<!-- start-section-[section-name] -->
## Section Title

Content goes here...
Can include code blocks like:
```code
your code here
```
<!-- end-section-[section-name] -->
```

### Lexorium v2.x.x Format
```markdown
## "Section Title"
<!-- start-section-[random-id] -->

Content goes here...
Can include code blocks like:
```code
your code here
```

<!-- end-section-[random-id] -->
```

## Output Format

Both versions generate JSON in this structure:

```json
{
  "version": "1.0",
  "sections": [
    {
      "id": "uniqueid1",
      "title": "Section Title",
      "content": "Content goes here...",
      "timestamp": "13.12.2024 - 19:51"
    }
  ]
}
```

## Requirements

- Python 3.x
- No additional dependencies required

## License

MIT License
