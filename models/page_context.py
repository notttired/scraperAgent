from models.page_element import PageElement
from dataclasses import dataclass
from typing import Dict, List, Any

@dataclass
class PageContext:
    url: str
    title: str
    elements: List[PageElement]
    navigation_history: List[str]
    current_goal: str
    extracted_data: Dict[str, Any]

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
