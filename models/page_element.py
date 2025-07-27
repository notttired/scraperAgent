from models.page_element import PageElement
from bs4 import Tag
from dataclasses import dataclass
from typing import Dict, List, Optional, cast

@dataclass
class PageElement:
    tag: str
    text: str
    attributes: Dict[str, str | List[str]]
    element_id: str
    clickable: bool
    visible: bool

def create_page_element(tag: Tag, base_url: str) -> PageElement:
    """Create PageElement from BeautifulSoup tag"""
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
