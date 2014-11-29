import os
import base64
import praw
from config_bot import REDDIT_PASSWORD, REDDIT_USERNAME, AGENT, SUBREDDIT, SEARCH_FOR, COMMENT


# Creates and authenticates session. Searches post title for text and replies to post if text is found.
def find_and_reply(text):
    reddit = praw.Reddit(user_agent=AGENT)
    reddit.login(REDDIT_USERNAME, base64.b64decode(REDDIT_PASSWORD))
    if not os.path.isfile("posts_replied_to.txt"):  # checks for existing list of posts replied to
        posts_replied_to = []
    else:
        with open("posts_replied_to.txt", "r") as uid_found:
            posts_replied_to = uid_found.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = filter(None, posts_replied_to)
    subreddit = reddit.get_subreddit(SUBREDDIT)
    for post in subreddit.get_new(limit=10):  # checks 10 newest posts and replies accordingly
        try:
            title = post.title
            if post.id not in posts_replied_to:
                if text.lower() in title.lower():
                    post.add_comment(COMMENT)
                    posts_replied_to.append(post.id)
        except praw.errors.RateLimitExceeded as error:
            print error
            break
        if len(posts_replied_to) > 0:
            with open("posts_replied_to.txt", "w") as uid_found:  # Write uid's to text file for future reference
                for post_id in posts_replied_to:
                    uid_found.write(post_id + "\n")

find_and_reply(SEARCH_FOR)