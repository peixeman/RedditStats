# Reddit Stats
A Tool for Statistically Analyzing Upvote Distributions on Reddit.com

Video expo: https://www.youtube.com/watch?v=79AYfRHLGSs

## Overview
This project allows users to procure subreddit upvote data and compare them against a known user's posts. This was inspired by YouTuber Based If True's observations about Reddit user u/Pizzacakecomic and her seemingly unusual popularity on r/comics.

### Libraries Used
* Matplotlib
* NumPy
* Pillow
* SciPy
* Selenium

Built-in packages:
* logging
* os
* pickle
* random
* Tkinter

## Example Files
https://drive.google.com/drive/folders/1xjQqln9XO3Zmmpg3Y_43HI9xS78hqbKb?usp=sharing

## Installation
Download a release and extract the files to any folder. Currently, this project is designed for and has been tested on Windows, though it may be possible for the Python files to function on Linux.

## Use
### Subreddit Sampling
To take a sample of a subreddit, enter the subreddit's name and how many desired bootstrap iterations you'd like. You may omit the "/r" from the name if you'd like. The recommended number of iterations is at least 1,000, but keep in mind that this process can take several hours to complete. Data will be saved to the "subreddit/SUBREDDIT_NAME/" directory.

### User Sampling
To take a sample of a user's posts on a subreddit, enter the subreddit's name, the user's name, and how many desired bootstrap iterations you'd like. You may omit the "/r" and "/u" from the names if you'd like. The recommended number of iterations is at least 1,000, but keep in mind that this process can take several hours to complete. Data will be saved to the "subreddit/SUBREDDIT_NAME/users/USER_NAME" directory.

NOTE: As of v1.0.0, the user's posts must be scoped to a subreddit.

### Results
Results can be viewed by clicking the "Display results" button. This new window will display a histogram and various statistics from the sample, including how high the bootstrap level is, the subreddit's mean and standard deviation, and the user's z-score and p-value. An automated conclusion will also be generated and displayed on the right-hand side of the window. A copy of the results and the image files will be saved to the "results" directory.

NOTE: These will be regenerated each time you choose to display.

## Tested Hardware
### Operating System
* Windows 10 64-bit
### CPU
* Intel Core i7-9700K
### GPU
* NVIDIA GeForce GTX 980 Ti
