from openai import OpenAI
import json
from dataclasses import dataclass
from typing import Dict, List, cast
from extractors.html_simplifier import PageContext, HTMLSimplifier
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class ActionType(Enum):
    CLICK = "click"
    SCROLL = "scroll"
    EXTRACT = "extract"
    SEARCH_PAGE = "search_page"
    NAVIGATE_TO = "navigate_to"
    COMPLETE = "complete"
    
@dataclass
class NavigationAction:
    action_type: ActionType
    target: str
    reasoning: str
    confidence: float
    metadata: Dict[str, str | List[str]] = {}

class NavigationPlanner:
    """LLM-based navigation planning"""
    
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client
        
    def get_next_action(self, page_context: PageContext) -> NavigationAction:
        """Plan next navigation action based on current page state"""
        
        html_simplifier = HTMLSimplifier()
        llm_context = html_simplifier.create_llm_context(page_context)
        
        system_prompt = """You are an intelligent web navigation assistant. Your task is to navigate websites to achieve specific goals."""

        prompt = f"""

{llm_context}

AVAILABLE ACTIONS:
1. CLICK - Click on a specific element (provide element number or description)
2. SCROLL - Scroll page (up/down)
3. EXTRACT - Extract specific data from current page
4. SEARCH_PAGE - Search for specific text/content on current page
5. NAVIGATE_TO - Navigate to a specific URL
6. COMPLETE - Goal achieved, extraction complete

TASK: {page_context.current_goal}

Based on the current page state, what should be the next action? Consider:
- Is the target content visible on current page?
- Are there navigation elements that might lead to the goal?
- What's the most logical next step?
- What would be the shortest path towards the goal?

Example response in JSON format:
{{
    "action_type": "CLICK|SCROLL|EXTRACT|SEARCH_PAGE|NAVIGATE_TO|COMPLETE",
    "target": "element_number_or_description",
    "reasoning": "why_this_action_makes_sense",
    "confidence": 0.8
}}
"""
        response = self.llm_client.chat.completions.create(
            model = "gpt-3.5-turbo",
            store = True,
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        parsed_response: Dict[str, str | float] = json.loads(response.choices[0].message.content or "")
        return self._create_navigation_action(parsed_response)
    
    def _create_navigation_action(self, action: Dict[str, str | float]):
        return NavigationAction(
            action_type = ActionType["action_type"],
            target = cast(str, action["target"]),
            reasoning = cast(str, action["reasoning"]),
            confidence = cast(float, action["confidence"])
        )
