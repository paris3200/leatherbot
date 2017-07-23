#!/usr/bin/env python

import praw
import time
import logging

"""
Config Settings
sub: The subreddit being moded.
bot: Name of the bot user
grace_period: Time in minutes to delete post that don't follow the rules
"""

sub = "Leathercraft"
bot = "leathercraft_automod"
grace_period = 60

# Setup logger
log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "moderation.log",
                    level = logging.DEBUG,
                    format = log_format)
logger = logging.getLogger()

# Authentication details setup in PRAW
reddit = praw.Reddit('bot1')



subreddit = reddit.subreddit(sub)
current_time = int(time.time())


def message(submission):
    submission.author.message(
        "Post Removal",
        "Your post has been automatically removed for violating \
        /r/leathercraft's Rules and Submissions Guidelines. Please take a \
        moment to familiarize with the rules, flair your post, and make sure \
        to include a top comment describing your project in detail."
        )


def delete_submission(submission):
    subreddit.mod.remove(submission)
    message(submission)
    print("Post Deleted /n")


def comment(submission, reply):
    if reply == "details":
        c = submission.reply(
        """Let's be honest, photo-only posts are a drag. We want details! Even if you've spent a lot of time writing a description on Imgur, etc. please take a moment and leave a top comment with a few details. It should include what you made, what you made it out of, and any other pertinent detailsthat will help the viewer understand what they're looking at.  \n\n  **Photo only posts without an OP comment will be automatically deleted after 1 hour.** """)

    elif reply == "flair":
        c = submission.reply("""/r/leathercraft requires you to flair your post!
                             This comment will be automatically deleted once
                             flair has been added. To add flair to your post,
                             open it and click the button labeled flair beneath
                             your title. From the menu, select the most appropriate category, and then hit save. You
                             do not need to delete or resubmit your post!""")
    elif reply == "both":
        c = submission.reply(
"""Congratulations on your post! Remember, /r/leathercraft requires you to flair your post! This comment will be automatically deleted once
flair has been added. If you haven't assigned flair yet, open it and click the button labeled flair beneath your title. From the menu, select
the most appropriate category, and then hit save.  You do not need to delete or resubmit your post!


And while we're on the topic, let's be honest-- photo-only posts are a drag. We want details! Even if you've spent a lot of time writing a
description on Imgur, etc. please take a moment and leave a top comment with a few details. It should include what you made, what you made it out
of, and any other pertinent details that will help the viewer understand what they're looking at.


**Photo only posts without an OP TOP COMMENT  will be automatically deleted after an hour.**""")

    else:
        print("Error:  Comment type not found.")

    c.mod.distinguish()


def main():
    for submission in subreddit.new(limit=1):
        logger.debug("Title:  %(submission.title)s")

        if submission.link_flair_text is None:
            flair = False
        else:
            flair = True

        author_comment = False
        auto_mod = False
        if sub not in submission.domain:
            for top_level_comment in submission.comments:
                if top_level_comment.author == submission.author:
                    author_comment = True
                if top_level_comment.author == bot:
                    auto_mod = True
                    mod_comment = top_level_comment

            age = (current_time - int(submission.created_utc)) / 60
            if author_comment is False and age > grace_period:
                logger.info("%(submission.title)s - Delete Submission")
                print("Delete Submission")
                delete_submission(submission)
            elif author_comment is False and auto_mod is False and flair is True:
                logger.info("%(submission.title)s - Warning - No Description")
                comment(submission, "details")
            elif author_comment is False and auto_mod is False and flair is False:
                logger.info("%(submission.title)s, \
                            - Warning - No Description or Flair")
                comment(submission, "both")
            elif author_comment is True and auto_mod is True and flair is True:
                logger.info("%(submission.title)s - Flair & Comment Detected - Delete Warning")
                mod_comment.delete()
            elif auto_mod is False and flair is False:
                logger.info("%(submission.title)s - Warning - No Flair")
                comment(submission, "flair")
        else:
            for top_level_comment in submission.comments:
                if top_level_comment.author == bot:
                    auto_mod = True
                    mod_comment = top_level_comment

            if auto_mod is True and flair is True:
                logger.info("%(submission.title)s - Flair Detected - Delete Warning")
                mod_comment.delete()
            elif auto_mod is False and flair is False:
                logger.info("%(submission.title)s - Flair Warning")
                comment(submission, "flair")

        print("-------------------------------------\n")


if __name__ == "__main__":
        main()
