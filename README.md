# websearch.py
Takes a variety of twitter user id's as a string and runs sentiment analysis for every user.
The program produces 4 numbers indicating the cumulative sentiment of a user's selected amount of tweets: negative, neutral, positive and compound
Modify the tweet_mode, count, and include_rts phrases in the get_timeline function to personalize your code.

Important Preparations Before Running the Code:
1) Install the python twitter package by using the following code:
  pip install python-twitter
2) Install the Vader NLTK package with the following command
  python -m nltk.downloader all
3) Open a Twitter developer account to have access to API's
4) Create an application from this link
  https://developer.twitter.com/en/apps
