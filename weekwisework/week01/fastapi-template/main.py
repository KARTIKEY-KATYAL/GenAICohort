from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import MsgPayload

app = FastAPI()
messages_list: dict[int, MsgPayload] = {}

# HTML templates
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            nav {{ margin-bottom: 20px; }}
            nav a {{ margin-right: 10px; }}
        </style>
    </head>
    <body>
        <nav>
            <a href="/">Home</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </nav>
        <h1>{title}</h1>
        <div>{content}</div>
    </body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    content = HTML_TEMPLATE.format(
        title="Home",
        content="Welcome to our FastAPI website!"
    )
    return content

@app.get("/about", response_class=HTMLResponse)
def about():
    content = HTML_TEMPLATE.format(
        title="About Us",
        content="This is a sample FastAPI application showcasing basic routing and HTML responses."
    )
    return content

@app.get("/contact", response_class=HTMLResponse)
def contact():
    content = HTML_TEMPLATE.format(
        title="Contact Us",
        content="Email us at: example@example.com<br>Phone: (123) 456-7890"
    )
    return content

# Route to add a message
@app.post("/messages/{msg_name}/")
def add_msg(msg_name: str) -> dict[str, MsgPayload]:
    # Generate an ID for the item based on the highest ID in the messages_list
    msg_id = max(messages_list.keys()) + 1 if messages_list else 0
    messages_list[msg_id] = MsgPayload(msg_id=msg_id, msg_name=msg_name)

    return {"message": messages_list[msg_id]}


# Route to list all messages
@app.get("/messages")
def message_items() -> dict[str, dict[int, MsgPayload]]:
    return {"messages:": messages_list}
