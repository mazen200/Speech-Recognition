import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3

# Function to handle speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio)
            text = text.lower()
            label_var.set(f"Recognized: {text}")
        except sr.UnknownValueError:
            label_var.set("Could not understand audio")
        except sr.RequestError:
            label_var.set("API unavailable")
        except Exception as e:
            label_var.set(f"Error: {str(e)}")

# Function to run speech recognition in a separate thread
def start_listening():
    threading.Thread(target=recognize_speech).start()

# Setting up the GUI
root = tk.Tk()
root.title("Speech Recognition Application")

label_var = tk.StringVar()
label_var.set("Press the button and speak")

label = tk.Label(root, textvariable=label_var, wraplength=400, justify="left")
label.pack(pady=20)

button = tk.Button(root, text="Start Listening", command=start_listening)
button.pack(pady=10)

root.mainloop()
