from models.page_context import PageContext, create_llm_context
from models.page_element import PageElement, create_page_element
from typing import Dict, List, Any, Optional, cast
from bs4 import BeautifulSoup, Tag


class HTMLSimplifier:
    """Converts HTML/BeautifulSoup to LLM-friendly representation"""
    
    def __init__(self, important_tags: List[str], content_tags: List[str]):
        self.important_tags = important_tags
        self.content_tags = content_tags
        
    def extract(self, html_content: str, base_url: str = "") -> List[PageElement]:
        """Extract relevant elements from page"""
        soup = BeautifulSoup(html_content, "lxml")
        elements: List[PageElement] = []
        
        interactive_tags = soup.find_all(self.important_tags)
        content_tags = soup.find_all(self.content_tags)
        
        significant_content_tags = [
            tag for tag in content_tags 
            if tag.get_text(strip=True) and len(tag.get_text(strip=True)) > 20
        ]
        
        # Combine all relevant tags
        all_relevant_tags = list(interactive_tags) + significant_content_tags
        
        # Process all tags
        for tag in all_relevant_tags:
            element = create_page_element(cast(Tag, tag), base_url)
            if element is not None:
                elements.append(element)
        
        return elements
