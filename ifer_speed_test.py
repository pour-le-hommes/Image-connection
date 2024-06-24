# Assuming you have llama-cpp installed and a pre-trained LLaMA model
import time
start_time = time.time()
import llama_cpp

# Initialize the model
model = llama_cpp.Llama(model_path="models/Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf")

# Define the prompt
prompt = "What can I do better?"

# Generate a response
response = model(prompt, max_tokens=800, stop=["", "</s>"], top_k=1, temperature=0.9)

# Print the response
print("Response:", response)


print("\n\nLlama-cpp time:",time.time()-start_time)