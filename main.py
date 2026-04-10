import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

API_KEY = os.getenv("API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_VERSION = "2024-02-01"
DEPLOYMENT_NAME = "gpt-4" 

try:
    client = AzureOpenAI(
      api_key=API_KEY,
      api_version=API_VERSION,
      azure_endpoint=AZURE_ENDPOINT
    )
    # A simple check to see if the client is configured
    if not API_KEY or API_KEY == "<YOUR_API_KEY_HERE>":
        print("🚨 API Key not found. Please set the DIAL_API_KEY environment variable or replace the placeholder in the code.")
    else:
        print("✅ Client initialized successfully!")
        print(client)
except Exception as e:
    print(f"🔥 Error initializing client: {e}")


def get_completion(messages, model=DEPLOYMENT_NAME):
    """
    Calls the OpenAI Chat Completions API and returns the message content.
    
    Args:
        messages (list): A list of message dictionaries (e.g., [{"role": "user", "content": "Hello"}]).
        model (str): The deployment name of the model to use.
        
    Returns:
        str: The content of the assistant's response.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

test_messages = [{"role": "user", "content": "Explain the concept of 'technical debt' in one sentence."}]
response_content = get_completion(test_messages)
print(response_content)

def classify_and_prioritize(ticket_text):
    """
    Classifies the support ticket into one of the following categories: 'Bug', 'Feature Request', 'Question', 'Praise', or 'Complaint'.
    Assigns a priority level: 'High', 'Medium', or 'Low'.
    Returns the assistant message text (intended to be a single JSON object with keys category and priority).
    """
    prompt = f"""
        You classify support tickets.

        Categories (use exactly one value for "category"): Bug, Feature Request, Question, Praise, Complaint.
        Priority (use exactly one value for "priority"): High, Medium, Low.

        Ticket:
        ```
        {ticket_text}
        ```

        Respond with exactly one JSON object and nothing else. The object must have only these two keys: "category" and "priority".
        Do not use markdown, code fences, or backticks. Do not add explanations or other keys.
        Example shape: {{"category": "Bug", "priority": "High"}}
    """
    messages = [{"role": "user", "content": prompt}]
    return get_completion(messages)

##Tests for classify_and_prioritize
print(classify_and_prioritize("The app crashes every time I try to upload a video."))
print(classify_and_prioritize("I can't seem to reset my password. The link you sent me has expired."))
print(classify_and_prioritize("I love the new feature that allows me to add multiple users to a project."))
print(classify_and_prioritize("The app is slow and I can't find the settings menu."))
print(classify_and_prioritize("Your support team does not respond to my emails."))
print(classify_and_prioritize("The app is slow and I can't find the settings menu."))
print(classify_and_prioritize("What are the steps to open a support ticket?"))
print(classify_and_prioritize("I am not able to run the print using sidebar but it works fine when i use print preview."))

def solve_logic_puzzle(puzzle):
    """
    Solves a logic puzzle and returns the solution.
    """
    prompt = f"""
    You are a puzzle-solving expert.

    You will be given a logic puzzle involving ordering or constraints. Your task is to determine the correct solution.

    Follow this structured approach internally:
    - Identify the key facts
    - Identify constraints/rules
    - Determine the goal
    - Derive the final arrangement

    Output requirements:
    1. Provide a brief, clear explanation of the reasoning (do not include step-by-step internal thoughts).
    2. Return the final answer as a list in order from front to back.
    3. Ensure the solution satisfies all constraints.

    Example:

    Puzzle:
    Four friends: Alex, Ben, Chris, David in a line;
    - Chris is not at either end
    - Ben is in front of Alex
    - David is behind Chris

    Answer:
    Explanation: Chris must be in a middle position. Ben must come before Alex, and David must come after Chris. The only arrangement satisfying all constraints is:
    Solution: [David, Chris, Ben, Alex]

    ---

Now solve the following logic puzzle:
    {puzzle}
    """
    messages = [{"role": "user", "content": prompt}]
    return get_completion(messages)

print(solve_logic_puzzle("""
Five friends: Ethan, Farhan, Gaurav, Harsh, Imran are standing in a line.

Gaurav is not at either end
Ethan appears before Farhan
Imran appears after Gaurav
Harsh is immediately in front of Gaurav
Farhan is not at the last position
"""))

def python_function_generator(description):
    """
    Generates a Python function based on the description.
    """
    prompt = f"""
    You are a Python function generator.
    You will be given a description of a Python function and you will need to generate the function.
    The function should be a valid Python function.

    Example:
    Description: Create a Python function named 'calculate_sum' that takes a list of numbers and returns their sum.

    Result:
    def calculate_sum(numbers):
        return sum(numbers)

    Use the description to generate the function between the ```python and ``` tags.

    Description: ```{description}```
    """

    messages = [{"role": "user", "content": prompt}]
    return get_completion(messages)

print(python_function_generator("Create a Python function named 'calculate_average' that takes a list of numbers and returns their average."))
print(python_function_generator("Create a Python function named 'calculate_percentage' that takes a score and a total score and returns the percentage."))


def parse_email_body(email_text):
    """
    Parses the email body and returns the primary contact information.
    """
    prompt = f"""
    You are a email parser.
    You will be given an email body and you will need to parse the email body and return the primary contact information.
    The email body will be delimited by ```email_body```

    The primary contact information is the name, email, and phone number of the sender.
    The name, email, and phone number should be returned as a JSON object.
    If a field is missing, use null.
    The JSON object should have the following keys: name, email, and phone.
    If no primary contact information is found, return None.
    Do not include any other text in the response.

    Email Body:
    ```
    {email_text}
    ```
    """
    messages = [{"role": "user", "content": prompt}]
    return get_completion(messages)

print(parse_email_body("""
    Hi Loyd,
    I hope this email finds you well.
    I am writing to you because I need help with my account.
    My account is not working and I need help to fix it.
    
    Regards,
    John Doe
    john.doe@example.com
    1234567890
    ```
    """))