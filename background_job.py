from facebook_scraper import get_posts as fb_get_posts
import pandas as pd
from db_conf import session
from models import Posts
from telegram_bot import send_image as tele_send_image, send_text as tele_send_text
import os
import requests

# Vars used throughout the entire file
# Get the words needed to be searched in the posts
words = pd.read_csv('words.csv')
# Get the pages needed to be scraped
pages = pd.read_csv('pages.csv')
# Seperate required words from blacklisted words (neglected words)
required_words = [x for x in words['Required'].tolist() if str(x) != 'nan']
neglected_words = [x for x in words['Neglected'].tolist() if str(x) != 'nan']
# Get posts ids that are stored in the db to check if they are already sent or not
old_posts = session.query(Posts.post_id).order_by(Posts.id.desc()).all()
old_posts_ids_as_list = [value for value, in old_posts]


def do_work():
    """Iterate through all pages and start work"""
    for _unused, page in pages.iterrows():
        handle_page_posts(page)


def handle_page_posts(page):
    """Get page posts, filter them, and send the valid ones"""
    fb_posts = fb_get_posts(page['Page_Id'], pages=2, timeout=40)
    newely_added_posts = get_required_posts(fb_posts)
    for post in newely_added_posts:
        send_post_on_telegram(post, page['Page_Name'])


def get_required_posts(fb_posts):
    """Check if a post is valid to be sent"""
    new_posts = []
    # Iterate through posts of a page
    for post in fb_posts:
        # Check validity
        if not is_a_wanted_post(post):
            continue
        # Check if the post is already sent
        if post['post_id'] in old_posts_ids_as_list:
            continue
        # Stack the new posts that should be sent
        new_posts.append(post)
    # Save new posts in db so it will not be sent in the next time
    save_new_posts_ids_to_db(new_posts)
    return new_posts


def is_a_wanted_post(post):
    """Check if a post is valid to be sent"""
    # Validate that the post has text
    if (post['text'] == "" or post['text'] is None):
        return False
    # Validate that the post has no blacklisted words
    if any(x in post['text'] for x in neglected_words):
        return False
    # Validate that the post has at least one required word
    if any(x in post['text'] for x in required_words):
        return True
    # If no condition is valid then it is considered as a neglected post
    return False


def save_new_posts_ids_to_db(new_posts):
    """Save newely added posts ids as bulk objects"""
    new_posts_objects = []
    for post in new_posts:
        new_db_post = Posts(post_id=post['post_id'])
        new_posts_objects.append(new_db_post)
    session.bulk_save_objects(new_posts_objects)
    session.commit()


def send_post_on_telegram(post, page_name):
    """Send message on the telegram bot including post text and image if exists"""
    # Prepare message text
    message_text = page_name + "\n \n" + post['text']
    # Get image if exists and send it through the bot
    if post['image'] in ("", None):
        temp_file = download_image(post['image'])
        tele_send_image(temp_file)
        os.remove(temp_file)
    # Send message text
    tele_send_text(message_text)


def download_image(link):
    """Download post image by link to be sent"""
    temp_file = "temp_image.png"
    response = requests.get(link)
    with open(temp_file, "wb") as file:
        file.write(response.content)
    return temp_file
