from flask import Flask, request, jsonify, render_template
from playwright.sync_api import sync_playwright
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder=".")

# OpenAI client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "YOUR_API_KEY_HERE"),
)

def extract_with_retry(url, context, retries=2):
    for attempt in range(retries):
        try:
            page = context.new_page()
            print(f"🔍 Loading tweet: {url} (attempt {attempt + 1})")
            page.goto(url, timeout=90000)
            page.wait_for_timeout(5000)

            content_elem = page.query_selector("article div[lang]")
            content = content_elem.inner_text().strip() if content_elem else "N/A"

            user_elem = page.query_selector("article a[role='link'][href*='/status/']")
            username = user_elem.get_attribute("href").split("/")[1] if user_elem else "unknown_user"

            date_elem = page.query_selector("article time")
            date = date_elem.get_attribute("datetime") if date_elem else None
            formatted_date = datetime.fromisoformat(date[:-1]).strftime('%B %d, %Y') if date else "Unknown date"

            page.close()

            return {
                "username": username,
                "date": formatted_date,
                "content": content
            }

        except Exception as e:
            print(f"⚠️ Error (attempt {attempt + 1}): {e}")
            time.sleep(1)  # Small wait before retry
            continue

    print(f"❌ Failed to extract tweet after {retries} attempts: {url}")
    return None

def extract_two_tweets(tweet_url_1, tweet_url_2):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-gpu",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-extensions",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-sync",
                "--mute-audio",
                "--metrics-recording-only",
                "--no-first-run",
                "--no-zygote",
                "--disable-dev-shm-usage",
                "--disable-software-rasterizer"
            ]
        )

        context = browser.new_context()
        try:
            tweet1 = extract_with_retry(tweet_url_1, context)
            tweet2 = extract_with_retry(tweet_url_2, context)
        finally:
            context.close()
            browser.close()

        return tweet1, tweet2

def detect_plagiarism(tweet1, tweet2):
    prompt = f"""
Compare two tweets and determine if one is plagiarized from the other. Use usernames and post dates for context.

Tweet by @{tweet1['username']} (Posted on {tweet1['date']}):
\"\"\"{tweet1['content']}\"\"\"

Tweet by @{tweet2['username']} (Posted on {tweet2['date']}):
\"\"\"{tweet2['content']}\"\"\"

Instructions:
- Determine which tweet (if any) appears to be copied.
- Reference the usernames directly (e.g., "@{tweet1['username']}'s tweet").
- Include a plagiarism score between 0 (no plagiarism) and 1 (extreme plagiarism).
- Base originality primarily on date and content similarity.

Return the result in this format:

🧠 Result:
### Comparison:
- Content similarity:
- Dates:
- Language/structure overlap:

### Verdict:
- Who appears to have posted the original:
- Who may have copied:

### Plagiarism Score:
- Score: X.XX (just a number from 0 to 1)


### Conclusion:
(Brief reasoning using usernames)
    """

    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in AI analysis: {e}")
        return f"Error analyzing tweets: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_tweets():
    data = request.json
    tweet_url_1 = data.get('tweet1')
    tweet_url_2 = data.get('tweet2')
    
    if not tweet_url_1 or not tweet_url_2:
        return jsonify({
            'success': False,
            'error': 'Please provide both tweet URLs'
        })  

    tweet1, tweet2 = extract_two_tweets(tweet_url_1, tweet_url_2)
    
    if tweet1 and tweet2:

        result = detect_plagiarism(tweet1, tweet2)

        return jsonify({
            'success': True,
            'tweet1': tweet1,
            'tweet2': tweet2,
            'analysis': result
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Could not extract both tweets'
        })

if __name__ == "__main__":
    app.run(debug=True)
