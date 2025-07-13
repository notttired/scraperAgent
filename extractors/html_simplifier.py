from typing import Dict, List, Any, Optional, cast
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
import logging

@dataclass
class PageElement:
    tag: str
    text: str
    attributes: Dict[str, str | List[str]]
    element_id: str
    clickable: bool
    visible: bool

@dataclass
class PageContext:
    url: str
    title: str
    elements: List[PageElement]
    navigation_history: List[str]
    current_goal: str
    extracted_data: Dict[str, Any]

class HTMLSimplifier:
    """Converts HTML/BeautifulSoup to LLM-friendly representation"""
    
    def __init__(self):
        self.important_tags = ['a', 'button', 'input', 'select', 'textarea', 'form', 'nav', 'menu', 'img']
        self.content_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'section', 'article']
        
    def extract_page_elements(self, soup: BeautifulSoup, base_url: str = "") -> List[PageElement]:
        """Extract relevant elements from page"""
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
            element = self._create_page_element(cast(Tag, tag), base_url)
            if element is not None:
                elements.append(element)
        
        return elements
    
    def _create_page_element(self, tag: Tag, base_url: str) -> Optional[PageElement]:
        """Create PageElement from BeautifulSoup tag"""
        try:
            text = tag.get_text(strip=True)[:200]  # May need to truncate long text
            attributes: Dict[str, str | List[str]]
            if tag.attrs:
                attributes = dict(tag.attrs)
            else:
                attributes = {}
            
            # Determine if clickable
            clickable = tag.name in ['a', 'button', 'input'] or \
                       'onclick' in attributes or \
                       'href' in attributes or \
                       'role' in attributes and attributes['role'] == 'button'
            
            # Determine id
            new_element_id: str = ""
            if isinstance(attributes.get("id"), str):
                new_element_id = cast(str, attributes.get("id"))
            
            return PageElement(
                tag=tag.name,
                text=text,
                attributes=attributes,
                element_id=new_element_id,
                clickable=clickable,
                visible=True
            )
        except Exception as e:
            logging.warning(f"Error creating element: {e}")
            return None
    
    def create_llm_context(self, page_context: PageContext) -> str:
        """Create LLM-friendly page representation"""
        context = f"""
CURRENT PAGE ANALYSIS:
URL: {page_context.url}
Title: {page_context.title}
Goal: {page_context.current_goal}
Navigation History: {' -> '.join(page_context.navigation_history)}

INTERACTIVE ELEMENTS:
"""
        
        clickable_elements = [e for e in page_context.elements if e.clickable]
        for i, element in enumerate(clickable_elements[:20]):  # Limit to top 20
            context += f"{i+1}. {element.tag.upper()}: '{element.text}' (href: {element.attributes.get('href', 'N/A')})\n"
        
        context += "\nCONTENT SECTIONS:\n"
        content_elements = [e for e in page_context.elements if not e.clickable and e.text]
        for i, element in enumerate(content_elements[:20]):  # Limit to top 20
            context += f"{i+1}. {element.tag.upper()}: {element.text[:100]}...\n"
        
        return context
