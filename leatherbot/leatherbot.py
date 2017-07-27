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

# Authentication details setup in PRAW
reddit = praw.Reddit('bot1')

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('moderation.log', mode='w')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

subreddit = reddit.subreddit(sub)
current_time = int(time.time())

FLAIR_WARNING = """
#### /r/leathercraft requires you to flair your post! ####

To add flair to your post, open it and click the button labeled flair beneath
your title. From the menu, select the most appropriate category, and then hit
save. You do not need to delete or resubmit your post!

This comment will be automatically deleted once flair has been added.
"""

DETAIL_WARNING = """
Let's be honest, photo-only posts are a drag. We want details! Even if you've
spent a lot of time writing a description on Imgur, etc. please take a moment
and leave a **top comment** with a few details. It should include what you made,
what you made it out of, and any other pertinent details that will help the
viewer understand what they're looking at.

**Photo only posts without an OP comment will be automatically deleted after
1 hour.**
"""

BOTH_WARNING = """
Congratulations on your post! Remember, /r/leathercraft requires you to flair
your post! This comment will be automatically deleted once flair has been added.
If you haven't assigned flair yet, open it and click the button labeled flair
beneath your title. From the menu, select the most appropriate category, and
then hit save.  You do not need to delete or resubmit your post!

And while we're on the topic, let's be honest-- photo-only posts are a drag. We
want details! Even if you've spent a lot of time writing a description on Imgur,
etc. please take a moment and leave a top comment with a few details. It should
include what you made, what you made it out of, and any other pertinent details
that will help the viewer understand what they're looking at.

**Photo only posts without an OP TOP COMMENT  will be automatically deleted
after an hour.**
"""

POST_REMOVAL = """
Your post has been automatically removed for violating /r/leathercraft's Rules
land Submissions Guidelines. Please take a moment to familiarize with the rules,
flair your post, and make sure to include a top comment describing your project
in detail."
"""

def message(submission):
    """
    Publishes a comment to Reddit stating why the post was removed.
    :param submission: The submission who's author should be messaged.
    """
    submission.author.message("Post Removal", POST_REMOVAL)

def delete_submission(submission):
    """
    Deletes the submission.
    :param submission: The Reddit Submission object to de deleted.
    """
    subreddit.mod.remove(submission)
    message(submission)
    logger.info("{} - Delete Submission".format(submission.title))


def comment(submission, reply):
    if reply == "details":
        c = submission.reply(DETAIL_WARNING)
        logger.info("%{} - Warning - No Description".format(submission.title))
    elif reply == "flair":
        c = submission.reply(FLAIR_WARNING)
        logger.info("{} - Warning - No Flair".format(submission.title))
    elif reply == "both":
        c = submission.reply(BOTH_WARNING)
        logger.info("{} - Warning - No Description or Flair".format(submission.title))
    else:
        logger.error("Error:  Comment type not found.")

    # Distininguishes the comment as an offical mod comment.
    c.mod.distinguish()


def main():
    for submission in subreddit.new(limit=20):
        logger.debug("Title: {}".format(submission.title))

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
                delete_submission(submission)

            elif author_comment is False and auto_mod is False and flair is True:
                comment(submission, "details")

            elif author_comment is False and auto_mod is False and flair is False:
                comment(submission, "both")

            elif author_comment is True and auto_mod is True and flair is True:
                mod_comment.delete()
                logger.info("{} - Flair & Comment Detected - Delete Warning".format(submission.title))

            elif auto_mod is False and flair is False:
                comment(submission, "flair")
        else:
            for top_level_comment in submission.comments:
                if top_level_comment.author == bot:
                    auto_mod = True
                    mod_comment = top_level_comment

            if auto_mod is True and flair is True:
                mod_comment.delete()
                logger.info("{} - Flair Detected - Delete Warning".format(submission.title))

            elif auto_mod is False and flair is False:
                comment(submission, "flair")


if __name__ == "__main__":
        main()
