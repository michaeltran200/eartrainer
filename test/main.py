import pygame
import random
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox

pygame.init()

# Define the notes we will use
notes = ["C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4", "C5"]

# Define the intervals we will quiz on
intervals = ["unison", "minor 2nd", "major 2nd", "minor 3rd", "major 3rd", "perfect 4th", "tritone", "perfect 5th", "minor 6th", "major 6th", "minor 7th", "major 7th", "octave"]

# Load the sound files
sounds = {}
for note in notes:
    sounds[note] = pygame.mixer.Sound(f"sounds\{note}.wav")

# Create the quiz window
quiz_window = tk.Tk()
quiz_window.title("Interval Ear Training")
quiz_window.geometry("700x700")

# Create the question label
question_label = tk.Label(
    quiz_window, 
    text="Welcome to Interval Ear Training! Click PLAY to Start.",
    font="Verdana",
    fg="seagreen",
    bg="white", 
    width=55
)

# Place the question label in the window 
question_label.grid(rowspan=2,
                    columnspan=2,
                    )

# Create the play button
play_button = tk.Button(quiz_window, text="PLAY", state=tk.NORMAL, width=12)
play_button.grid(row=0,
                 column=3,
                 padx=5,pady=2)

# Create a progress bar for the sound
pb = ttk.Progressbar(quiz_window,
                     orient="horizontal",
                     mode="determinate", 
                     length=500)
pb.grid(row=3,
        columnspan=2)

# Answer buttons will change color upon hover
def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", func=lambda e: button.config(bg=colorOnHover))
    button.bind("<Leave>", func=lambda e: button.config(bg=colorOnLeave))

# Create the answer buttons
answer_buttons = []
for interval in intervals:
    button = tk.Button(quiz_window, text=interval, state=tk.DISABLED, width=20, 
                       command=lambda i=interval: check_answer(i),
                       pady=5, bg="whitesmoke")
    answer_buttons.append(button)

# Place the answer buttons in a grid
x = 4
for button in answer_buttons:
        button.grid(row=x,
                columnspan=3,
                pady=5)
        x += 1

# Create the score labels
correct_label = tk.Label(quiz_window, 
                         text="Correct: 0", 
                         bg="lightgreen", width=12)
correct_label.grid(row=3,
                   column=3, 
                   padx=5)

incorrect_label = tk.Label(quiz_window, 
                           text="Incorrect: 0", 
                           bg="lightcoral",  width=12)
incorrect_label.grid(row=4,
                   column=3, 
                   padx=5)


# Global variables
current_question = 1
total_questions = 12
correct_answers = 0
incorrect_answers = 0
note1 = "C4"
note2 = ""
random_interval = ""
sound_length = 1000
sound_waittime = 600

# Define the function to play the two notes
def choose_interval():
    global note1, note2

    pygame.mixer.stop()
    # Pick a random note
    note2 = random.choice(notes)

    # Return the interval between the two notes
    return intervals[notes.index(note2) - notes.index(note1)]

# Define the function to replay the interval
def play_interval():
    global note1, note2, sound_waittime

    # Start the progress bar
    pb.start

    # Play the first note
    sounds[note1].play()

    # Delay the playing of the second note
    pygame.time.wait(sound_waittime)

    # Play the second note
    sounds[note2].play()

    #Stop the progress bar
    pb.stop

# Create the replay button
replay_button = tk.Button(quiz_window, text="Replay Interval", state=tk.DISABLED, command=play_interval, width=12)
replay_button.grid(row=1,
                   column=3,
                   pady=2,)

# Define the function to start a new question
def start_new_question():
    global current_question, correct_answers, incorrect_answers, random_interval

    # Disables Play button
    play_button["state"] = tk.DISABLED

    # Choose the interval after updating the UI
    random_interval = choose_interval()

    # Play the interval
    play_interval()

    # Update the question label
    question_label["text"] = f"Question {current_question}/{total_questions}: \nWhat is the interval between C4 and the second note?"

    # Enable answer buttons
    for button in answer_buttons:
        button["state"] = tk.NORMAL
        changeOnHover(button, "lightblue", "whitesmoke")

    # Enable replay button
    replay_button["state"] = tk.NORMAL

# Play button will start game once pressed
play_button["command"] = start_new_question

# Define the function to check the selected answer
def check_answer(selected_interval):
    global current_question, correct_answers, incorrect_answers, random_interval

    # Disable answer buttons
    for button in answer_buttons:
        button["state"] = tk.DISABLED

    # Disable replay button
    replay_button["state"] = tk.DISABLED

    # Update the score labels
    correct_label["text"] = f"Correct: {correct_answers}"
    incorrect_label["text"] = f"Incorrect: {incorrect_answers}"
    
    # Check the selected answer
    if selected_interval == random_interval:
        messagebox.showinfo("Result", f"Correct! The interval is {random_interval}.")
        correct_answers += 1
    else:
        messagebox.showerror("Result", f"Incorrect! The interval is {random_interval}.")
        incorrect_answers += 1

    # Update the score labels
    correct_label["text"] = f"Correct: {correct_answers}"
    incorrect_label["text"] = f"Incorrect: {incorrect_answers}"

    # Check if the quiz is finished
    if current_question == total_questions:
        tk.messagebox.showinfo("Quiz Finished", f"""The quiz is finished. 
Your score: {correct_answers}/{total_questions}! 
The program will now close.""")
        quiz_window.destroy()
    else:
        # Move to the next question
        current_question += 1
        start_new_question()

# Run the GUI main loop
quiz_window.mainloop()