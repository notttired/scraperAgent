from navigators.base_navigator import BaseNavigator
from models.navigation_action import NavigationAction, create_navigation_action
from models.page_context import PageContext, create_llm_context

from openai import OpenAI
import json
from typing import Dict

class BasicNavigator(BaseNavigator):
    def __init__(self, llm_client: OpenAI):
        self.llm_client = llm_client

    def plan(self, page_context: PageContext) -> NavigationAction:
        """Plan next navigation action based on current page state"""
        
        llm_context = create_llm_context(page_context)
        
        system_prompt = """You are an intelligent web navigation assistant. Your task is to navigate websites to achieve specific goals."""

        prompt = f"""

{llm_context}

AVAILABLE ACTIONS:
1. NAVIGATE_TO - Navigate to a specific URL
2. COMPLETE - Goal achieved, on desired webpage

TASK: {page_context.current_goal}

Based on the current page state, what should be the next action? Consider:
- Is the target content visible on current page?
- Are there navigation elements that might lead to the goal?
- What's the most logical next step?
- What would be the shortest path towards the goal?

Example response in JSON format:
{{
    "action_type": "NAVIGATATE_TO",
    "target": "element_number",
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
        return create_navigation_action(parsed_response)
