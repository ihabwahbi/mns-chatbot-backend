import time
import json
from openai import OpenAI
from dotenv import load_dotenv
from utils.database.db_manager import get_material_info

# Load environment variables from .env file
load_dotenv()

# Initialize the client
client = OpenAI()  # It will automatically pick up OPENAI_API_KEY from environment


def openai_handle_initial_msg(prompt, thread_id=None):
    print("User Question: ", prompt)
    if thread_id is None:
        # Create a new thread
        thread = client.beta.threads.create()
        thread_id = thread.id
        print("New thread id has been created ", thread_id)
    else:
        print("Using existing thread id ", thread_id)

    # Add message to thread
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=prompt
    )

    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id="asst_kyAjRCF6whOx2mQYep81sDf0",
    )

    # Loop until run status is 'requires_action' or 'completed'
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        status = run.status
        print("Current status is " + status)

        if status == "requires_action":
            break
        elif status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            ai_initial_response = messages.data[0].content[0].text.value
            print("AI Initial Response is: ", ai_initial_response)
            return ai_initial_response, thread_id
        elif status == "failed":
            raise Exception(f"Run failed: {run.last_error}")
        elif status == "expired":
            raise Exception("Run expired")
        else:
            time.sleep(2)

    # Handle tool calls
    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_outputs = []

    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        arguments = json.loads(tool_call.function.arguments)
        part_number = arguments.get("part_number")

        if part_number:
            print("Input to db function: ", part_number)
            db_output = str(get_material_info(part_number))
            tool_outputs.append({"tool_call_id": tool_call_id, "output": db_output})

    # Submit tool outputs
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id, run_id=run.id, tool_outputs=tool_outputs
    )

    # Wait for final response
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        status = run.status
        print("Current status is " + status)

        if status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            manager_message = messages.data[0].content[0].text.value
            print(manager_message)
            return manager_message, thread_id
        elif status == "failed":
            raise Exception(f"Run failed: {run.last_error}")
        elif status == "expired":
            raise Exception("Run expired")
        else:
            time.sleep(2)
