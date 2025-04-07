import os
import google.generativeai as genai

genai.configure(api_key="")

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You are an AI Chatbot: 'AeroAI' provideing information and support for drones and arial vehicles.act as a drone expert, sharing informative facts with the asked questions\n",
)

history=[]
print("Hi, I am AeroAI, your drone expert!")
while True:

    user_input = input("You: ")

    Chat_session = model.start_chat(
     history=history
    
    )

    response = Chat_session.send_message(user_input)

    model_response = response.text

    print(f'AeroAI: {model_response}')
    print()

    history.append({"role":"user","parts":[user_input]})
    history.append({"role":"user","parts":[model_response]})
