from datetime import datetime
from functools import partial
import io
import threading
import customtkinter
import cv2
from functions.gemini_functions import text_generation
from functions.tts_functions import tts
from PIL import Image, ImageTk
import time
import asyncio

Gemini = text_generation()
TTS = tts()

Gemini.init_model()
TTS.init_model()

response = ""

def update_camera(label):
    ret, frame = cap.read()
    if ret:
        frame = frame[:, :, ::-1]
        img = Image.fromarray(frame)
        Gemini._lastimage = img
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
    label.after(10, update_camera, label)

def generate_tts():
    TTS.tts(Gemini._lastresponse)



customtkinter.set_appearance_mode("dark") #dark
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1600x800")

frame = customtkinter.CTkFrame(master=root)
frame.pack(fill="both", expand=True)

# Create the camera label
camera_label = customtkinter.CTkLabel(master=frame, height=32, width=10,text="")
camera_label.pilimage = None
camera_label.pack(pady=12, padx=10)

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create the entry widget and place it at the bottom center
entry1 = customtkinter.CTkTextbox(frame, font=("Plus Jakarta Sans", 24),text_color="white",width=1500,height=400)
entry1.pack( pady=12, padx=10,side="bottom",anchor="s")


entry1.insert("0.0", "Initiating...")

# Start the camera update loop
update_camera(camera_label)

# Gemini._lastresponse = "Alright, so you're just chilling in a tank top, looking pretty relaxed.  You're probably just hanging out, maybe doing some work or just taking a break.  You look cool and comfortable"

def stream_text(textbox=entry1):
    textbox.delete("0.0", "end")
    response = Gemini._lastresponse
    for i in response.split(" "):
        textbox.insert("end", i)
        textbox.insert("end", " ")
        time.sleep(0.1)

def cyclic_task():
    while True:
        if TTS._finished ==True:
            
            threading.Thread(target=Gemini.generate_response).start()

            if response == Gemini._lastresponse:
                print("Sleeping time")
                time.sleep(4)
            else:
                TTS._finished = False
                print("Response var:",response,"\n\n\n")
                print("Last response var:",Gemini._lastresponse,"\n\n\n")
                threading.Thread(target=stream_text, args=(entry1,)).start()
                threading.Thread(target=generate_tts).start()
                
                calc_sleep = len([i for i in Gemini._lastresponse.split(" ")])//3
                time.sleep(calc_sleep+5)  # Wait for additional 5 seconds before the next cycle

threading.Thread(target=cyclic_task).start()

root.mainloop()


# Release the video capture object and close OpenCV windows when done
cap.release()
cv2.destroyAllWindows()
