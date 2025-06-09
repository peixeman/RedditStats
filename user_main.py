import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import numpy as np
import os
import pickle
import logging

def main(subreddit, user, num_of_iterations):
    # Selenium setup
    driver = webdriver.Chrome()

    # Loads random words
    r = np.array([])
    with open("resources/words.txt", "r") as file:
        for line in file:
            r = np.append(r, line.strip())

    # numpy array setup
    means_of_trials = np.array([])

    # Creates user directory if it does not exist
    try:
        os.makedirs(f"subreddits/{subreddit.lower()}/users")
        logging.info(f"Creating directory /{subreddit.lower()}/users")
    except FileExistsError:
        logging.debug(f"Users directory already exists")
        print(f"Users directory already exists")

    # Opens output text file
    output_file = open(f"subreddits/{subreddit.lower()}/users/{user.lower()}_means.txt", "a")

    # Loads existing pickle file data
    try:
        with open(f"subreddits/{subreddit.lower()}/users/{user.lower()}_means.pkl", "rb") as pkl_file:
            pickle_stats = pickle.load(pkl_file)
    except (FileNotFoundError, EOFError):
        with open(f"subreddits/{subreddit.lower()}/users/{user.lower()}_means.pkl", "wb") as pkl_file:
            logging.info("Creating user data (.pkl) file")
            pickle.dump("", pkl_file)
            pickle_stats = np.array([])

    # Counts requests made to old.reddit
    requests = 0

    # Bootstraps random searches
    for iterations in range(num_of_iterations):
        # Resets array
        upvote_scores_array = np.empty(shape=0, dtype=int)
        i = 0
        while i < 30:
            # If HTTP Error 429 occurs, Selenium window is reopened
            try:
                driver.implicitly_wait(0)
                fail = driver.find_element(By.ID, "main-frame-error")
            except selenium.common.exceptions.NoSuchElementException:
                fail = None
            if fail:
                logging.info("Restarting ChromeDriver...")
                print("Restarting ChromeDriver...")
                driver.close()
                driver = webdriver.Chrome()

            # "Shuffles" results
            sorting_method = random.randint(1, 5)
            if sorting_method == 1:
                sort_by = "relevance"
            elif sorting_method == 2:
                sort_by = "top"
            elif sorting_method == 3:
                sort_by = "new"
            elif sorting_method == 4:
                sort_by = "comments"
            else:
                sort_by = "hot"

            # Request searches old.reddit using parameters
            driver.get(
                f"https://old.reddit.com/r/{subreddit}/search?q={str(r[random.randrange(len(r))])}%2C+author%3Au%2F{user}&restrict_sr=on&sort={sort_by}&t=all")
            driver.implicitly_wait(5)
            requests += 1

            try:
                if "search-score" in driver.page_source:
                    # Cleans string
                    score = driver.page_source.split("search-score\">", 1)[-1].split("</span>", 1)[0].rstrip(
                        " points").rstrip(" point").replace(",", "")
                    # Appends upvote score to array
                    upvote_scores_array = np.append(upvote_scores_array, int(score))
                    i += 1
            except selenium.common.exceptions.NoSuchWindowException as err:
                logging.error(f"Window prematurely closed: {err}")
                print("Window prematurely closed")

            # Tracks requests
            logging.info(f"Number of requests made: {requests}")
            print(f"Number of requests made: {requests}")

        # Appends mean to array and wipes
        means_of_trials = np.append(means_of_trials, upvote_scores_array.mean())
        pickle_stats = np.append(pickle_stats, upvote_scores_array.mean())
        logging.info(f"Iterations: {iterations + 1}")
        print(f"Iterations: {iterations + 1}")

        # Writes sample mean to txt and pkl files
        output_file.write(f"{upvote_scores_array.mean()}\n")
        output_file.flush()
        with open(f"subreddits/{subreddit}/users/{user}_means.pkl", "wb") as pkl_file:
            pickle.dump(pickle_stats, pkl_file)

    # Closes resources
    output_file.close()
    driver.close()

if __name__ == "__main__":
    main()