import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import re  # For text formatting
from PIL import Image, ImageTk  # To add an icon

# Configure Google Gemini API
genai.configure(api_key="AIzaSyDbIgzhjCHhUIngbwrZ_inB4HhTK5ghlSM")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Function to send a message
def send_message():
    user_text = user_input.get()
    if not user_text.strip():
        return

    chat_box.config(state=tk.NORMAL)
    insert_message(f"You: {user_text}", "user")
    user_input.delete(0, tk.END)

    chat_box.insert(tk.END, "\nAeroAI is typing...", "bot")
    chat_box.update()

    response = model.start_chat(history=[]).send_message(user_text).text

    chat_box.delete("end-2l")
    insert_bot_response(response)

    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# Function to insert bot response with formatting
def insert_bot_response(response):
    insert_message("AeroAI: ", "bot")
    
    bold_matches = list(re.finditer(r"\*\*(.*?)\*\*", response))
    last_index = 0
    formatted_response = ""

    for match in bold_matches:
        start, end = match.span()
        formatted_response += response[last_index:start]
        formatted_response += f"<bold>{match.group(1)}</bold>"
        last_index = end

    formatted_response += response[last_index:]
    formatted_response = re.sub(r"(?m)^\s*\*", "•", formatted_response)

    segments = re.split(r"(<bold>.*?</bold>)", formatted_response)

    for segment in segments:
        if segment.startswith("<bold>") and segment.endswith("</bold>"):
            chat_box.insert(tk.END, segment[6:-7], "bold")
        else:
            chat_box.insert(tk.END, segment, "bot")

    chat_box.insert(tk.END, "\n\n", "bot")

# Function to insert messages into the chat box
def insert_message(message, tag):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, message + "\n", tag)
    chat_box.config(state=tk.DISABLED)
    chat_box.yview(tk.END)

# Function to change button color on hover
def animate_button(event):
    send_button.config(bg="#ffcc00", fg="black")

def reset_button(event):
    send_button.config(bg="#ff9500", fg="black")

# Function to clear chat
def clear_chat():
    chat_box.config(state=tk.NORMAL)
    chat_box.delete("1.0", tk.END)
    chat_box.config(state=tk.DISABLED)

# Create the main UI window
root = tk.Tk()
root.title("AeroAI - Drone Chatbot")
root.geometry("650x650")
root.configure(bg="#1e1e1e")
root.resizable(True, True)

# Load AeroAI Logo
try:
    logo_image = Image.open("aeroai_logo.png").resize((50, 50))
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(root, image=logo_photo, bg="#1e1e1e")
    logo_label.place(x=20, y=10)
except:
    pass

# Title Label
title_label = tk.Label(root, text="AeroAI", font=("Cfour", 20, "bold"), fg="#ff9500", bg="#1e1e1e")
title_label.place(x=80, y=20)

# Clear Chat Button
clear_button = tk.Button(root, text="Clear Chat", command=clear_chat, font=("Helvetica", 12), bg="red", fg="white")
clear_button.place(x=500, y=10)

# Frame for Chatbox
chat_frame = tk.Frame(root, bg="#1e1e1e", padx=10, pady=10)
chat_frame.pack(pady=(80, 10), padx=10, fill="both", expand=True)

# Chatbox
chat_box = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 12))
chat_box.config(bg="#252525", fg="white", state=tk.DISABLED, padx=10, pady=5, bd=2, relief="flat")
chat_box.tag_config("user", foreground="lightblue", font=("Helvetica", 12, "bold"))
chat_box.tag_config("bot", foreground="lightgreen", font=("Helvetica", 12))
chat_box.tag_config("bold", font=("Helvetica", 12, "bold"))
chat_box.pack(fill="both", expand=True)

# Frame for input and button
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(pady=10, padx=10, fill="x")

# User Input Field
user_input = tk.Entry(input_frame, width=55, font=("Helvetica", 12), bg="#2e2e2e", fg="white", insertbackground="white", bd=2, relief="flat")
user_input.pack(side=tk.LEFT, padx=5, ipadx=5, ipady=5, fill="x", expand=True)

# Send Button
send_button = tk.Button(input_frame, text="Send", font=("Helvetica", 12, "bold"), bg="#ff9500", fg="black", activebackground="#ff7300", relief="flat", command=send_message)
send_button.pack(side=tk.RIGHT, padx=5, ipadx=10, ipady=5)
send_button.bind("<Enter>", animate_button)
send_button.bind("<Leave>", reset_button)

# Function to display welcome message
def welcome_message():
    insert_message("AeroAI: Hello! How can I assist you with drones today?", "bot")

root.after(1000, welcome_message)

# Run the application
root.mainloop()
