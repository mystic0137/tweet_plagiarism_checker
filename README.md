# Twitter plagiarism checker

A web application that analyzes pairs of tweets to detect potential plagiarism. The tool extracts tweet content, usernames, and posting dates, then uses AI to determine if one tweet was copied from another.

## Features

- Extract tweet content and metadata directly from Twitter URLs
- Compare two tweets for content similarity and chronological order
- Generate a plagiarism score from 0 (no plagiarism) to 1 (extreme plagiarism)
- Provide detailed analysis of tweet similarities and differences
- User-friendly web interface for quick analysis

## Technologies Used

- **Flask**: Web application framework
- **Playwright**: Browser automation for tweet extraction
- **OpenAI API** (via OpenRouter): AI-powered plagiarism detection
- **Python-dotenv**: Environment variable management
- **Gunicorn**: WSGI HTTP server for production deployment
- **Render**: Cloud deployment platform

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tweet_plagiarism_checker.git
cd tweet_plagiarism_checker
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers and system dependencies:
```bash
chmod +x build.sh
./build.sh
```

## Configuration

1. Create a `.env` file in the project root
2. Add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

You can obtain an API key by registering at [OpenRouter](https://openrouter.ai/).

## Usage

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter two tweet URLs in the provided input fields

4. Click "Analyze Tweets" to see the comparison results

The analysis will include:
- Content similarity assessment
- Chronological comparison of posting dates
- Language and structure overlap analysis
- Overall plagiarism score
- Final verdict on which tweet appears to be original

## How It Works

1. **Tweet Extraction**: The application uses Playwright to visit the provided URLs and extract the tweet content, username, and posting date.

2. **Plagiarism Detection**: The extracted data is sent to the DeepSeek Chat model via OpenRouter API with a prompt that:
   - Compares the content of both tweets
   - Considers posting dates to determine chronological precedence
   - Evaluates language and structural similarities
   - Generates a plagiarism score on a scale from 0 to 1

3. **Result Presentation**: The analysis is formatted and displayed to the user through the web interface

## Deployment

The project is configured for deployment on Render.com using the provided `render.yaml` file:

```bash
# For local deployment with Gunicorn
gunicorn wsgi:app --timeout 180
```

For Render.com deployment:
1. Connect your GitHub repository to Render
2. Render will automatically use the configuration in `render.yaml`
3. Add your `OPENROUTER_API_KEY` as an environment variable in the Render dashboard

## Project Structure

- `app.py`: Main Flask application with routes and tweet analysis logic
- `build.sh`: Script to install Playwright and system dependencies
- `index.html`: Frontend interface for the application
- `requirements.txt`: Python dependencies
- `render.yaml`: Configuration for Render.com deployment
- `wsgi.py`: WSGI entry point for production servers

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

