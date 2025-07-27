url = "redlobster.ca"
goal = "Please find an image of their menu in full" # In proper english

important_tags = ['a', 'button', 'input', 'select', 'textarea', 'form', 'nav', 'menu', 'img']
content_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'div', 'section', 'article']
concurrency_limit = 10

browser_args = {
    "headless": False
}

llm_client_args = {}
