from llama_cpp import Llama
from opensource_functions import Hermes

hermes = Hermes()
hermes.init()

messages = [
                { "role": "system", "content": f"""
You are a helpful assistant.
""" }
            ]

user_prompt = input("User: ")

messages.append({"role": "user","content": user_prompt})

while user_prompt!="stop":

    resp = hermes.prompt(messages)

    messages.append({"role": "assistant","content": resp})

    user_prompt = input("Users: ")
    
    messages.append({"role": "user","content": user_prompt})