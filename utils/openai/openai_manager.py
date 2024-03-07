import time
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from utils.database.db_manager import get_material_info

# Load environment variables from .env file
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def openai_handle_initial_msg(prompt, thread_id=None):
    print("User Question: ", prompt)
    if thread_id is None:
        # No thread_id was provided, create a new thread
        thread = client.beta.threads.create()
        thread_id = thread.id
        print("New thread id has been created ", thread_id)
    else:
        # Use the provided thread_id
        print("Using existing thread id ", thread_id)

    # Add message to Thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )
    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id='asst_kyAjRCF6whOx2mQYep81sDf0',
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
            ai_initial_response = messages.data[0].content[0].text.value
            print("AI Initial Response is: ", ai_initial_response)
            return ai_initial_response, thread_id
        else:
            # If not, wait for some time before checking again
            time.sleep(2)  # Wait for 2 seconds

    tool_calls = run.required_action.submit_tool_outputs.tool_calls
    tool_call_id_all = []  # List to store tool_call_ids
    part_number_all = [] 
    po_number_all = []

    # Iterate over each tool call
    for tool_call in tool_calls:
        tool_call_id = tool_call.id
        tool_call_id_all.append(tool_call_id)

        # Extracting and printing model for each tool call
        arguments = tool_call.function.arguments
        arguments_parsed = json.loads(arguments)
        part_number = arguments_parsed.get('part_number')

        if part_number:
            part_number_all.append(part_number)

    # Now tool_call_ids list contains all the tool_call_ids
    print("All tool call IDs:", tool_call_id_all)

    # And models list contains all the models
    print("Part Numbers: ", part_number_all)

    print("Input to db function: ", part_number_all[0])
    db_output = str(get_material_info(part_number_all[0]))

    run = client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread_id,
    run_id=run.id,
    tool_outputs=[{
            "tool_call_id": tool_call_id,
            "output": db_output
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
            return manager_message, thread_id
        else:
            # If not, wait for some time before checking again
            time.sleep(2)  # Wait for 2 seconds
    