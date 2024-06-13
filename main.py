import tkinter as tk
import threading
import speech_recognition as sr

# Global variables
listening = False
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Function to handle speech recognition
def recognize_speech():
    global listening
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        while listening:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                text = recognizer.recognize_google(audio)
                text = text.lower()
                label_var.set(f"Recognized: {text}")
            except sr.WaitTimeoutError:
                if not listening:
                    break
            except sr.UnknownValueError:
                label_var.set("Could not understand audio")
            except sr.RequestError:
                label_var.set("API unavailable")
            except Exception as e:
                label_var.set(f"Error: {str(e)}")
            if not listening:
                break

# Function to start speech recognition in a separate thread
def start_listening():
    global listening
    listening = True
    button_start.config(bg="#ff6f61", activebackground="#ff5f50")
    button_stop.config(state=tk.NORMAL)
    threading.Thread(target=recognize_speech).start()

# Function to stop speech recognition
def stop_listening():
    global listening
    listening = False
    button_start.config(bg="#008CBA", activebackground="#007bb5")
    button_stop.config(state=tk.DISABLED)

# Setting up the GUI
root = tk.Tk()
root.title("Speech Recognition Application")
root.geometry('800x500')
root.configure(bg='#2c3e50')

# Project title label
title_label = tk.Label(root, text="Speech Recognition Application", font=("Helvetica", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
title_label.pack(pady=20)

label_var = tk.StringVar()
label_var.set("Press the button and speak")

# Recognized text label
label_frame = tk.Frame(root, bg="#34495e", padx=10, pady=10, bd=5, relief="groove")
label_frame.pack(pady=20, fill="x", padx=20)
label = tk.Label(label_frame, textvariable=label_var, wraplength=700, justify="left", bg="#34495e", fg="#ecf0f1", font=("Helvetica", 16))
label.pack()

# Button frame
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=20)

# Start Listening button
button_start = tk.Button(button_frame, text="Start Listening", command=start_listening, bg="#008CBA", fg="#ecf0f1", activebackground="#007bb5", font=("Helvetica", 16), relief="raised", width=15)
button_start.grid(row=0, column=0, padx=10)

# Stop Listening button
button_stop = tk.Button(button_frame, text="Stop Listening", command=stop_listening, bg="#4CAF50", fg="#ffffff", activebackground="#c0392b", font=("Helvetica", 16), relief="raised", width=15, state=tk.DISABLED)
button_stop.grid(row=0, column=1, padx=10)

root.mainloop()
