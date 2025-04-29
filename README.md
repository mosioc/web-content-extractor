# Web Content Extractor

A lightweight Python utility for extracting the core content from web pages and saving it as clean HTML files. This tool preserves important elements like paragraphs, code blocks, inline code sections, images, and tables while removing clutter.

![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Content Focused**: Extracts the main content while removing ads, navigation bars, footers, and other distractions
- **Format Preservation**: Maintains formatting for code blocks, inline code, tables, and other specialized content
- **Styling**: Adds minimal CSS to ensure readability and proper formatting
- **Error Handling**: Gracefully handles connection issues and invalid URLs
- **Customizable**: Simple command-line interface with options for output file specification

## Requirements

- Python 3.6+
- BeautifulSoup4
- Requests

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/web-content-extractor.git
   cd web-content-extractor
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

   Or install dependencies manually:
   ```bash
   pip install beautifulsoup4 requests
   ```

## Usage

### Basic Usage

Extract content from a URL and save it with an auto-generated filename:

```bash
python conex.py https://example.com
```

### Specify Output File

```bash
python conex.py https://example.com -o output.html
```

### Using as a Module

You can also import and use the functions in your own Python code:

```python
from conex import extract_web_content, extract_core_content, enhance_content_preservation, save_content_html

# Get content from a URL
soup = extract_web_content("https://example.com")

# Extract the core content
core_content = extract_core_content(soup)

# Enhance the content preservation
enhanced = enhance_content_preservation(core_content)

# Save to a file
output_path = save_content_html(enhanced, "https://example.com", "output.html")
print(f"Content saved to: {output_path}")
```

## 🔍 How It Works

1. **Request**: Sends a request to the specified URL with a standard User-Agent header
2. **Parse**: Uses BeautifulSoup to parse the HTML content
3. **Clean**: Removes unnecessary elements like scripts, styles, and navigation
4. **Extract**: Identifies the main content container using content-specific heuristics
5. **Preserve**: Maintains the original content structure and formatting
6. **Style**: Adds minimal CSS to ensure proper display of code blocks, tables, etc.
7. **Save**: Outputs the extracted content as a clean HTML file

## Function Reference

### `extract_web_content(url)`
Fetches and parses a web page, removing scripts and style elements.

### `extract_core_content(soup)`
Identifies and extracts the main content container from the parsed HTML.

### `enhance_content_preservation(soup)`
Ensures special elements like code blocks and tables are properly preserved.

### `save_content_html(content, url, output_path=None)`
Saves the extracted content as an HTML file.

## Customization

The script uses heuristics to identify the main content area, looking for common identifiers like:
- Elements with IDs containing: 'content', 'main', 'article', 'post', 'entry'
- Elements with classes containing similar terms

You can modify these heuristics in the `extract_core_content()` function to better match specific websites you're targeting.

## 📄 License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/new-feature`)
3. Commit your changes (`git commit -m 'Add some new feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request. 
