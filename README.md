# Facebook-Posts-in-Telegram
 
Python scripts to get posts from specific facebook pages (predefined pages in "pages.csv") and send them through a Telegram bot.

The posts are classified as needed or not depending on some keywords (also predefined in "words.csv"), keywords are used to neglect posts or consider them as useful.


## Installation & Usage
1. Clone the repo
  ```sh
   git clone https://github.com/uka7/Facebook-Posts-in-Telegram.git
  ```
2. Create a virtual environment
  ```sh
   cd Facebook-Posts-in-Telegram
   python3 -m venv env
  ```
3. Activate the virtual environment
  ```sh
   source env/bin/activate
  ```
4. Install packages
  ```sh
   pip install -r requirements.txt 
  ```
5. Set TOKEN & CHAT_ID in telegram_bot.py

6. Set required facebook pages and keywords in pages.csv and words.csv

7. Run
  ```
   python main.py
  ```

# Notes
- The existing data in pages.csv and words.csv extracts discounts and offers from Iraqi restaurants pages.
- This Telegram channel is using this bot to post new messages https://t.me/DiscountsIQ (Check it out !).
- The script should be run every period of time to get the new posts (Like a cronjob).
