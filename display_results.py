import numpy as np
import numpy._core._exceptions
import matplotlib.pyplot as plt
import pickle
import logging

def main(subreddit, user):
    # Loads subreddit data from file
    means_of_s_trials = np.array([])
    try:
        with open(f"subreddits/{subreddit.lower()}/{subreddit.lower()}_means.pkl", "rb") as file:
            means_of_s_trials = pickle.load(file)
    except Exception as err:
        logging.warning(err)
        print(err)

    # Loads user data from file
    try:
        with open(f"subreddits/{subreddit.lower()}/users/{user.lower()}_means.pkl", "rb") as file:
            means_of_u_trials = pickle.load(file)
    except Exception as err:
        logging.warning(err)
        print(err)

    # Combines data for visualization scaling
    combined_data = np.concatenate((means_of_s_trials, means_of_u_trials))

    # Histogram of subreddit results using matplot
    plt.hist(means_of_s_trials, bins=15, edgecolor="black")
    plt.title(f"Distribution of Upvotes from r/{subreddit}")
    plt.savefig("results/subreddit_result.png")
    plt.close()

    # Histogram of user results
    plt.hist(means_of_u_trials, bins=15, edgecolor="black")
    plt.title(f"Distribution of Upvotes from u/{user} on r/{subreddit}")
    plt.savefig("results/user_result.png")
    plt.close()

    # Combined histogram
    try:
        plt.hist(means_of_s_trials, range=(combined_data.min(), combined_data.max()), bins=20, edgecolor="black")
        plt.hist(means_of_u_trials, range=(combined_data.min(), combined_data.max()), bins=20, edgecolor="black")
    except numpy._core._exceptions.UFuncTypeError as err:
        logging.error(err)
        print(err)
    else:
        plt.title(f"Mean Upvotes on r/{subreddit} vs.\nMean Upvotes of u/{user} on r/{subreddit}")
        plt.savefig("results/combined_result.png")
        plt.close()

    # Loads results into dictionary to pass into window
    try:
        results_dict = {
            "sub_mean": float(means_of_s_trials.mean()),
            "sub_std": float(means_of_s_trials.std()),
            "sub_bootstrap_amount": len(means_of_s_trials),
            "user_mean": float(means_of_u_trials.mean()),
            "user_std": float(means_of_u_trials.std()),
            "user_bootstrap_amount": len(means_of_u_trials)
        }
    except TypeError as err:
        logging.error(err)
        print(err)
        return None

    return results_dict

if __name__ == "__main__":
    main()