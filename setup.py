from setuptools import setup, find_packages

setup(
    name="mns-chatbot-backend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "openai",
        "python-dotenv",
        # Add other dependencies
    ],
)
