from models.action_type import ActionType
from models.navigation_action import NavigationAction
from models.page_context import PageContext, create_llm_context
from models.page_element import PageElement

from openai import OpenAI
import json
from dotenv import load_dotenv
from typing import Dict, List, cast


load_dotenv()

class NavigationPlanner:
    """LLM-based navigation planning"""
    
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client
        
    def get_next_action(self, page_context: PageContext) -> NavigationAction:
        """Plan next navigation action based on current page state"""
        
        llm_context = create_llm_context(page_context)
        
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
