import subreddit_main as sbr
import user_main as usr
import display_results as dsp
from tkinter import *
from scipy.stats import norm
from PIL import Image, ImageTk
import os
import logging

# Ensures logs folder exists
if not os.path.exists("logs"):
    try:
        os.mkdir("logs")
    except:
        exit(-1)

# Log setup
logging.basicConfig(filename="logs/main.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def display_error_dialog(message):
    logging.error(message)

    # Instantiates error window
    error_window = Toplevel(window)
    error_window.geometry("200x60")
    error_window.title("Error")

    # Button
    Label(error_window, text=message).pack()
    Button(error_window, text="Ok", command=error_window.destroy).pack()

    error_window.mainloop()

def sbr_button_press():
    # Launches subreddit_main.main() if checks pass
    if txt1.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter subreddit")
    elif txt1_i.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter number of\nbootstrap iterations")
    else:
        sbr.main(txt1.get("1.0", "end-1c").strip().lstrip("r/"), int(txt1_i.get("1.0", "end-1c").strip()))

def usr_button_press():
    # Launches user_main.main() if checks pass
    if txt1.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter subreddit")
    elif txt2.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter user")
    elif txt2_i.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter number of\nbootstrap iterations")
    else:
        usr.main(txt1.get("1.0", "end-1c").strip().lstrip("r/"), txt2.get("1.0", "end-1c").strip().lstrip("u/"), int(txt2_i.get("1.0", "end-1c").strip()))

def launch_button_press():
    # Launches subreddit_main.main() and user_main.main() if checks pass
    if txt1.get("1.0", "end-1c") == "" or\
            txt1_i.get("1.0", "end-1c") == "" or\
            txt2.get("1.0", "end-1c") == "" or \
            txt2_i.get("1.0", "end-1c") == "":
        display_error_dialog("Please fill in all options")
    else:
        sbr.main(txt1.get("1.0", "end-1c").strip().lstrip("r/"), int(txt1_i.get("1.0", "end-1c").strip()))
        usr.main(txt1.get("1.0", "end-1c").strip().lstrip("r/"), txt2.get("1.0", "end-1c").strip().lstrip("u/"), int(txt2_i.get("1.0", "end-1c").strip()))

def display_button_press():
    # Launches display_results.main() if checks pass
    if txt1.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter subreddit")
    elif txt2.get("1.0", "end-1c") == "":
        display_error_dialog("Please enter user")
    else:
        # Checks if data exists
        try:
            open(f"subreddits/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}_means.txt", "r")
        except FileNotFoundError:
            display_error_dialog("Could not read subreddit data")
            return

        try:
            open(f"subreddits/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}/users/{txt2.get("1.0", "end-1c").strip().lstrip("u/")}_means.txt", "r")
        except FileNotFoundError:
            display_error_dialog("Could not read user data")
            return

        results_dict = dsp.main(txt1.get("1.0", "end-1c").strip().lstrip("r/"), txt2.get("1.0", "end-1c").strip().lstrip("u/"))

        # Error handling
        if results_dict is None:
            display_error_dialog("Matplot could not generate figure")
            return

        # Loads results image
        image = Image.open("results/combined_result.png")
        photo = ImageTk.PhotoImage(image)
        width, height = image.size

        # Instantiates results window
        results_window = Toplevel(window)
        results_window.geometry(f"{width + 560}x{height + 150}")
        results_window.title("Results")

        # Calculates z-score of user
        z_score = (results_dict["user_mean"] - results_dict["sub_mean"]) / results_dict["sub_std"]

        # Finds p-value using scipy stats
        p_value = norm.sf(z_score)

        # Conclusion
        conclusion_message = f"Since p-value = {p_value}, which is "
        if p_value < 0.05:
            conclusion_message += f"< α = 0.05, the null hypothesis is rejected.\n"
            conclusion_message += f"There is a significant difference between the distribution of post upvotes on r/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}\n"
            conclusion_message += f"the distribution of u/{txt2.get("1.0", "end-1c").strip().lstrip("u/")}'s posts' upvotes on r/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}."
        else:
            conclusion_message += f"> α = 0.05, the null hypothesis is not rejected.\n"
            conclusion_message += f"There is no significant difference between the distribution of post upvotes on r/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}\n"
            conclusion_message += f"the distribution of u/{txt2.get("1.0", "end-1c").strip().lstrip("u/")}'s posts' upvotes on r/{txt1.get("1.0", "end-1c").strip().lstrip("r/")}."

        # Shows results on screen
        label = Label(results_window, image=photo)
        label.image = photo
        label.grid(row=0, column=0, padx=10)
        Label(results_window, text=f"Subreddit boostrap level: {results_dict["sub_bootstrap_amount"]}").grid(row=1, column=0, padx=10)
        Label(results_window, text=f"User boostrap level: {results_dict["user_bootstrap_amount"]}").grid(row=2, column=0, padx=10)
        Label(results_window, text=f"μ: {results_dict["sub_mean"]}").grid(row=3, column=0, padx=10)
        Label(results_window, text=f"σ: {results_dict["sub_std"]}").grid(row=4, column=0)
        Label(results_window, text=f"z-score: {z_score}").grid(row=5, column=0, padx=10)
        Label(results_window, text=f"p-value: {p_value}").grid(row=6, column=0, padx=10)
        Label(results_window, text=conclusion_message).grid(row=0, column=1, padx=10)

        # Outputs metrics and conclusion to file
        with open("results/results.txt", "w", encoding="utf-8") as file:
            file.write(f"Subreddit boostrap level: {results_dict["sub_bootstrap_amount"]}\n")
            file.write(f"User boostrap level: {results_dict["user_bootstrap_amount"]}\n")
            file.write(f"μ: {results_dict["sub_mean"]}\n")
            file.write(f"σ: {results_dict["sub_std"]}\n")
            file.write(f"z-score: {z_score}\n")
            file.write(f"p-value: {p_value}\n")
            file.write(conclusion_message)

# Instantiates instance of window
window = Tk()
window.geometry("690x400")
window.title("Reddit Stats")
icon = PhotoImage(file="resources/reddit_stats_logo.png")
window.iconphoto(True, icon)

# Textbox1 label and text
lbl1 = Label(window, text="Enter subreddit:")
lbl1.grid(row=0, column=0, padx=10, pady=5)

txt1 = Text(window, height=2, width=40)
txt1.grid(row=1, column=0, padx=10, pady=5)

# Textbox1 iterations label, text, and button
lbl1_i = Label(window, text="Enter desired number of bootstrap iterations:")
lbl1_i.grid(row=2, column=0, padx=10, pady=5)

txt1_i = Text(window, height=2, width=40)
txt1_i.grid(row=3, column=0, padx=10, pady=5)

btn = Button(window, text="Launch subreddit sampling", command=sbr_button_press)
btn.grid(row=4, column=0, padx=10, pady=20)

# Textbox2 label and text
lbl2 = Label(window, text="Enter reddit username:")
lbl2.grid(row=0, column=1, padx=10, pady=5)

txt2 = Text(window, height=2, width=40)
txt2.grid(row=1, column=1, padx=10, pady=5)

# Textbox2 iterations label, text, and button
lbl2_i = Label(window, text="Enter desired number of bootstrap iterations:")
lbl2_i.grid(row=2, column=1, padx=10, pady=5)

txt2_i = Text(window, height=2, width=40)
txt2_i.grid(row=3, column=1, padx=10, pady=5)

btn = Button(window, text="Launch user sampling", command=usr_button_press)
btn.grid(row=4, column=1, padx=10, pady=20)

# Launch both samplings label and button
launch_both = Label(window, text="Launch both samplings, first subreddit then user")
launch_both.grid(row=5, column=0, padx=10, pady=5)

btn = Button(window, text="Launch both", command=launch_button_press)
btn.grid(row=6, column=0, padx=10, pady=5)

# Display results label and button
launch_both = Label(window, text="Click to display histograms of results")
launch_both.grid(row=5, column=1, padx=10, pady=5)

btn = Button(window, text="Display results", command=display_button_press)
btn.grid(row=6, column=1, padx=10, pady=5)

# Places window and listens for events
window.mainloop()