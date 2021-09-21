from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#FCD8D4"
YELLOW = "#FDF6F0"
L_ORANGE = "#F8E2CF"
ORANGE = "#F5C6AA"
RED = "#e7305b"
GREEN = "#57837B"

COLOR_L_BREAK = ORANGE
COLOR_BREAK = L_ORANGE
COLOR_FOCUS = PINK
COLOR_DEFAULT = YELLOW

FONT_NAME = "Courier"

WORK_MIN = 0.2
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 0.15

TIMER = None
reps = 0

MODE = "CAN_CHANGE"
# ---------------------------- WINDOW SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.after(1000)

# ---------------------------- TIMER LABEL ------------------------------- #
timer_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
timer_label.grid(row=1, column=2)

# ---------------------------- START BUTTON ------------------------------- #


def start_timer():
    global MODE
    MODE = "Start_Timer"
    global reps
    reps += 1

    # Long Break
    if reps % 8 == 0:
        window.config(bg=COLOR_L_BREAK)
        canvas.config(bg=COLOR_L_BREAK)
        timer_label.config(text="WALK", bg=COLOR_L_BREAK)
        label_task.config(bg=COLOR_L_BREAK)
        check = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            check += "✔"
        label_check.config(text=f"{check}", bg=COLOR_L_BREAK)

        count_down(60*LONG_BREAK_MIN)
    # Short Break
    elif reps % 2 == 0:
        window.config(bg=COLOR_BREAK)
        canvas.config(bg=COLOR_BREAK)
        timer_label.config(text="BREAK", bg=COLOR_BREAK)
        label_task.config(bg=COLOR_BREAK)
        check = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            check += "✔"
        label_check.config(text=f"{check}", bg=COLOR_BREAK)

        count_down(60 * SHORT_BREAK_MIN)
    # Focus Mode
    else:
        window.config(bg=COLOR_FOCUS)
        canvas.config(bg=COLOR_FOCUS)
        timer_label.config(text="WORK", bg=COLOR_FOCUS)
        label_task.config(bg=COLOR_FOCUS)
        label_check.config(bg=COLOR_FOCUS)

        count_down(60*WORK_MIN)


start_button = Button(text="Start Time", command=start_timer, width=8, highlightthickness=0)
start_button.grid(row=3, column=1)

# ---------------------------- BREAK BUTTON ------------------------------- #


def break_timer():
    global MODE
    MODE = "Break_Timer"
    window.after_cancel(TIMER)
    window.config(bg=COLOR_BREAK)
    canvas.config(bg=COLOR_BREAK)
    timer_label.config(text="BREAK", bg=COLOR_BREAK)
    label_task.config(bg=COLOR_BREAK)
    check = ""
    work_session = math.floor(reps / 2)
    for _ in range(work_session):
        check += "✔"
    label_check.config(text=f"{check}", bg=COLOR_BREAK)

    count_down(60 * SHORT_BREAK_MIN)


button_break = Button(text="Start Break", width=8, highlightthickness=0, command=break_timer)
button_break.grid(row=4, column=1)

# ---------------------------- RESET BUTTON ------------------------------- #


def reset_button():
    global MODE
    MODE = "Reset_Timer"
    window.after_cancel(TIMER)
    canvas.itemconfig(timer_text, text="00:00")
    canvas.config(bg=COLOR_DEFAULT)
    window.config(bg=COLOR_DEFAULT)
    timer_label.config(text="Timer", bg=COLOR_DEFAULT)
    label_task.config(bg=COLOR_DEFAULT)
    label_check.config(bg=COLOR_DEFAULT)


button_reset = Button(text="Reset Time", width=8, highlightthickness=0, command=reset_button)
button_reset.grid(row=3, column=2)

# ---------------------------- STOP BUTTON ------------------------------- #


def stop_button():
    global MODE
    MODE = "Stop_Timer"
    count_down()


button_stop = Button(text="Stop Timer", width=8, highlightthickness=0, command=stop_button)
button_stop.grid(row=3, column=3)

# ---------------------------- ADD TASK LABEL AND BUTTON ------------------------------- #
def entry_button():
    task_name = entry_add_task.get()
    label_task.config(task=task_name)

entry_add_task = Entry(width=15, highlightthickness=0)
entry_add_task.insert(END, string="Enter your task")
entry_add_task.grid(row=4, column=3)

# ---------------------------- TASK LABEL ------------------------------- #
label_task = Label(text="Task I am working on", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 16, "bold"))
label_task.grid(row=5, column=2)

# ---------------------------- REPS CHECKS LABEL ------------------------------- #
label_check = Label(fg=RED, bg=YELLOW, font=(FONT_NAME, 14, "bold"))
label_check.grid(row=4, column=2)

# ---------------------------- CANVAS ------------------------------- #
tomato_image = PhotoImage(file="tomato.png")
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
canvas.create_image(100, 112, image=tomato_image)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=2, column=2)

# ---------------------------- COUNTDOWN FUNCTION ------------------------------- #
def count_down(count):
    global MODE
    global TIMER
    count_min = math.floor(count / 60)
    count_sec = count % 60
    filler_sec = ""
    filler_min = ""
    if count_sec == 0:
        count_sec = "00"
    elif count_sec < 10:
        filler_sec = "0"
    if count_min < 10:
        filler_min = "0"

    canvas.itemconfig(timer_text, text=f"{filler_min}{count_min}:{filler_sec}{count_sec}")
    if count > 0 and (MODE == "Start_Timer" or MODE == "Break_Timer"):
        TIMER = window.after(1000, count_down, count-1)
    elif count >= 0 and MODE == "Stop_Timer":
        TIMER = window.after(0, count_down, count)
    else:
        start_timer()


window.mainloop()