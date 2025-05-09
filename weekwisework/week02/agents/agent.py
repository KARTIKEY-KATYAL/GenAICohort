from openai import OpenAI
from dotenv import load_dotenv
import requests 
import os,json

load_dotenv()

client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))


def run_command(command):
    print("🔨 Tool Called: run_command")
    result = os.system(command=command)
    return result

def get_weather(city: str):
    print("🔨 Tool Called: get_weather")
    
    url = f"http://wttr.in/{city}?format=%C+%t"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather of {city} is {response}"
    
    return "Weather not found"

def add_numbers(numbers: list) -> int:
    print("🔨 Tool Called: add_numbers")
    return sum(numbers)

avaiable_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a command as input to execute on system and returns ouput"
    },
    "add_numbers" : {
        "fn" : add_numbers,
        "description" : "return s sum of all numbers in the array"
    }
}


SYSTEM_PROMPT = f""""
    You are an helpful AI Assistant who is specialized in resolving user query.
    You work on start, plan, action, observe mode.
    For the given user query and available tools, plan the step by step execution, based on the planning,
    select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.

    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    
    Available Tools :
    - Get Weather - To get Weather by api call
    - Run Command - To run any command on the terminal
    - Add Numbers = To add geiven nos in the array

    Output JSON Format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function",
    }}

    Available Tools:
    - get_weather: Takes a city name as an input and returns the current weather for the city
    - run_command: Takes a command as input to execute on system and returns ouput
    - add_numbers: Takes a array of numbers and return their sum
    
    Example:
    User Query: What is the weather of new york?
    Output: {{ "step": "plan", "content": "The user is interseted in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools I should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees." }}
"""


while True :
    user_query = input("> ")

    messages = [
        {"role" : "system" , "content" : SYSTEM_PROMPT}
    ]

    messages.append({"role" : "user" , "content" : user_query})

    while True:
        result = client.chat.completions.create(
            model='gpt-4o',
            messages=messages
        )
        
        parsed_output = json.loads(result.choices[0].message.content)
        messages.append({"role" : "assistant" , "content" : json.dumps(parsed_output)})
        
        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            if avaiable_tools.get(tool_name, False) != False:
                output = avaiable_tools[tool_name].get("fn")(tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output":  output}) })
                continue
        
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break

