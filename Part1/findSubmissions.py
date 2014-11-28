import praw
import datetime

agent = "redditBot 0.1 by DJO"

reddit = praw.Reddit(user_agent = agent)
subreddit = reddit.get_subreddit("learnpython")

for submission in subreddit.get_hot(limit = 5):
    print "Title: ", submission.title
    print "Text: ", submission.selftext
    print "Created: ", datetime.datetime.fromtimestamp(submission.created)
    print "---------------------------------\n"

