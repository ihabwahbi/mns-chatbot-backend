from utils.openai.openai_manager import openai_handle_initial_msg


def test_openai():
    prompt = "Hello, what is the status of H115576?"
    openai_handle_initial_msg(prompt)


if __name__ == "__main__":
    test_openai()
