import os
import base64
import praw
from config_bot import REDDIT_PASSWORD, REDDIT_USERNAME, AGENT, SUBREDDIT, SEARCH_TITLE, COMMENT, SEARCH_COMMENT, REPLY


# Finds text in a set of posts and replies.
def find_post_and_reply(text):
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
        if len(posts_replied_to) > 0:  # Write uid's to text file for future reference
            history = len(posts_replied_to)
            with open("posts_replied_to.txt", "w") as uid_found:
                for post_id in posts_replied_to:
                    uid_found.write(post_id + "\n")
    return "Total posts found to date: {}".format(history)

# Finds text in a set of comments and replies.
def find_comment_and_reply(comments, text):
    reddit = praw.Reddit(user_agent=AGENT)
    reddit.login(REDDIT_USERNAME, base64.b64decode(REDDIT_PASSWORD))
    if not os.path.isfile("comments_replied_to.txt"):  # checks for existing list of comments replied to
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as comment_found:
            comments_replied_to = comment_found.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = filter(None, comments_replied_to)
    for comment in comments:
        try:
            if SEARCH_COMMENT in comment.body and commenit.id not in comments_replied_to: # all comments
                comment.reply(REPLY)
                comments_replied_to.append(comment.id)
        except praw.errors.RateLimitExceeded as error:
            print error
            break
        if len(comments_replied_to) > 0:  # Write uid's to text file for future reference
            history = len(posts_replied_to)
            with open("comments_replied_to.txt", "w") as comment_found:
                for comment_id in comments_replied_to:
                    comment_found.write(comment_id + "\n")
    return "Total posts found to date: {}".format(history)

find_post_and_reply(SEARCH_TITLE)
#find_comment_and_reply(comments, SEARCH_COMMENT)
