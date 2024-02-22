import time
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key="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")

def openai_handle_initial_msg(prompt):
    print("User Question: ", prompt)
    thread = client.beta.threads.create()
    thread_id = thread.id
    print("New thread id has been created ", thread_id)
    # Add message to Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id='asst_qRU2rF6oUfYLJEVOHOnXT4FM',
    )
    # Loop until run status is 'requires_action' or 'completed'
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        status = run.status
        print("Current status is " + status)
        # Check if the status is 'requires_action'
        if status == "requires_action":
            # If it is, break the loop
            break
        elif status == "completed":
            # If status is 'completed', retrieve messages and then exit
            messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            manager_message = messages.data[0].content[0].text.value
            print(manager_message)
            return manager_message
        else:
            # If not, wait for some time before checking again
            time.sleep(2)  # Wait for 2 seconds

    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_call_ids = []  # List to store tool_call_ids
    po_numbers = []  # List to store models

    # Iterate over each tool call
    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        tool_call_ids.append(tool_call_id)

        # Extracting and printing model for each tool call
        arguments = tool_call.function.arguments
        arguments_parsed = json.loads(arguments)
        po_number = arguments_parsed['po_number']
        po_numbers.append(po_number)

    # Now tool_call_ids list contains all the tool_call_ids
    print("All tool call IDs:", tool_call_ids)

    # And models list contains all the models
    print("All POs: ", po_numbers)

    run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread_id,
    run_id=run.id,
    tool_outputs=[{
            "tool_call_id": tool_call_id,
            "output": "correct"
        }]
    )

    # Loop until run status is 'complete'
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        status = run.status
        print("Current status is " + status)
        # Check if the status is 'complete'
        if status == "completed":
            # Display the Assistant Response
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            manager_message = messages.data[0].content[0].text.value
            print(manager_message)
            return manager_message
        else:
            # If not, wait for some time before checking again
            time.sleep(2)  # Wait for 2 seconds
    