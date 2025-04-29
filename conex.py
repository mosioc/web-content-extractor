import requests
from bs4 import BeautifulSoup
import os
import argparse
from urllib.parse import urlparse


def extract_web_content(url):
    """
    Extract core content from a web page
    
    Args:
        url (str): URL of the web page to extract content from
        
    Returns:
        BeautifulSoup object: The parsed HTML content
    """
    # Add User-Agent header to avoid blocking
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'iframe', 'nav', 'footer', 'aside']):
            script_or_style.decompose()
            
        return soup
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None


def extract_core_content(soup):
    """
    Extract the main content from the parsed HTML
    
    Args:
        soup (BeautifulSoup): The parsed HTML
    
    Returns:
        BeautifulSoup object: The extracted core content
    """
    if not soup:
        return None
    
    # Try to find main content containers
    # This is a heuristic approach as different websites have different structures
    content_candidates = []
    
    # Look for common content containers
    main_candidates = soup.find_all(['main', 'article', 'div'])
    
    for candidate in main_candidates:
        # Check for common content identifiers
        if candidate.get('id') and any(term in candidate.get('id').lower() for term in ['content', 'main', 'article', 'post', 'entry']):
            content_candidates.append((candidate, 3))
        if candidate.get('class'):
            class_str = ' '.join(candidate.get('class')).lower()
            if any(term in class_str for term in ['content', 'main', 'article', 'post', 'entry']):
                content_candidates.append((candidate, 2))
    
    # If we found potential content containers, use the highest scored one
    if content_candidates:
        content_candidates.sort(key=lambda x: x[1], reverse=True)
        main_content = content_candidates[0][0]
    else:
        # Fallback: use body if no better container found
        main_content = soup.body
    
    # Create a new soup with just our content
    new_soup = BeautifulSoup('<html><head><meta charset="utf-8"></head><body></body></html>', 'html.parser')
    
    # Copy the content
    new_soup.body.append(main_content)
    
    return new_soup


def save_content_html(content, url, output_path=None):
    """
    Save the extracted content as HTML
    
    Args:
        content (BeautifulSoup): The content to save
        url (str): Original URL (used for title if available)
        output_path (str, optional): Path to save the HTML file
    
    Returns:
        str: Path to the saved file
    """
    if not content:
        return None
    
    # Try to get the title
    title_tag = content.find('title')
    if title_tag:
        title = title_tag.text.strip()
    else:
        # Use the domain name as fallback title
        parsed_url = urlparse(url)
        title = parsed_url.netloc
    
    # Create safe filename
    safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in title)
    safe_title = safe_title[:50]  # Limit length
    
    # Determine output path
    if not output_path:
        output_path = f"{safe_title}.html"
    
    # Save the file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(str(content))
    
    return output_path


def enhance_content_preservation(soup):
    """
    Enhance content preservation by ensuring code blocks and other special elements
    are properly maintained.
    
    Args:
        soup (BeautifulSoup): The parsed HTML content
        
    Returns:
        BeautifulSoup: Enhanced HTML content
    """
    if not soup:
        return None
    
    # Add a basic CSS style to preserve formatting
    style_tag = soup.new_tag('style')
    style_tag.string = """
    pre, code {
        background-color: #f6f8fa;
        border-radius: 3px;
        font-family: monospace;
        padding: 0.2em 0.4em;
        overflow-x: auto;
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    pre {
        padding: 16px;
        line-height: 1.45;
    }
    img {
        max-width: 100%;
        height: auto;
    }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    table, th, td {
        border: 1px solid #ddd;
        padding: 8px;
    }
    """
    
    # Add the style to the head
    if soup.head:
        soup.head.append(style_tag)
    else:
        head = soup.new_tag('head')
        head.append(style_tag)
        soup.html.insert(0, head)
    
    return soup


def main():
    """Main function to run the script from command line"""
    parser = argparse.ArgumentParser(description='Extract core content from a web page and save as HTML')
    parser.add_argument('url', help='URL of the web page to extract content from')
    parser.add_argument('-o', '--output', help='Output file path')
    args = parser.parse_args()
    
    print(f"Extracting content from: {args.url}")
    
    # Extract and process content
    soup = extract_web_content(args.url)
    if not soup:
        print("Failed to extract content")
        return
    
    core_content = extract_core_content(soup)
    if not core_content:
        print("Failed to find core content")
        return
    
    # Enhance content preservation
    enhanced_content = enhance_content_preservation(core_content)
    
    # Save the content
    output_path = save_content_html(enhanced_content, args.url, args.output)
    
    if output_path:
        print(f"Content successfully saved to: {output_path}")
    else:
        print("Failed to save content")


if __name__ == "__main__":
    main()