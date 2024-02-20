from utils.openai.openai_manager import openai_handle_initial_msg

def test_openai():
    prompt = "What is the status of PO 4569994542?"
    openai_handle_initial_msg(prompt)

if __name__ == "__main__":
    test_openai()