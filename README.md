# Scrapple

A self-hosted Reddit scraper with a web interface that lets you create custom feeds from Reddit search results.

## Why Scrapple Exists

Reddit doesn't natively support creating a customized feed of only search results—you're stuck with the default algorithmic feed or manually searching every time. While Reddit offers RSS feeds, there's no guarantee that support will continue. **Scrapple** solves this by letting you:

- Create saved searches and get fresh results on demand
- Build a personal feed of exactly what you're looking for
- Self-host everything, so you own your data and aren't dependent on external services
- Run scrapes manually or on a schedule (coming in the future)

Whether you're researching niche communities, monitoring specific topics, or building a personalized news feed, Scrapple puts you in control.

## How it Started

Scrapple was originally a bootcamp final project. Since then I decided to do a complete overhaul of the app and migrate to Django. My hope is that people find it useful, and that it can fill a gap that Reddit has left in it's user interface.

## Features

- **Search Management**: Create and manage multiple saved searches
- **Post Feed**: Browse scraped posts in a clean, paginated interface
- **Filtering**: Filter the feed by search or view all posts
- **Self-Hosted**: Run everything locally or on your own server—no third-party accounts needed
- **REST API**: Programmatic access to searches and scraping

## Future Plans

- **Reddit Scraping**: Extract posts from specific subreddits or across all of Reddit
- **Timed Updates**: Automatically run scrapes on a schedule you set (hourly, daily, weekly, etc.)
- **Enhanced UI**: Richer features for managing and exploring your feeds
- **Modern Frontend**: A new React-based interface for a better user experience

## Installation

### Prerequisites

You'll need **Python 3.8 or higher** installed on your computer. If you don't have it, download it from [python.org](https://www.python.org/downloads/).

### Step-by-Step Setup

#### 1. Download the Project

Clone the repository to your computer:

```bash
git clone https://github.com/gaspar-ericmartin/scrapple.git
cd scrapple
```

Or download it as a ZIP file from GitHub, then extract it to a folder on your computer.

#### 2. Create a Virtual Environment

A virtual environment keeps dependencies isolated for this project. Run:

```bash
python -m venv venv
```

#### 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` appear in your terminal prompt.

#### 4. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

#### 5. Set Up the Database

Django uses a SQLite database by default. Initialize it:

```bash
python manage.py migrate
```

#### 6. Create an Admin Account (Optional)

If you want to access the Django admin panel:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a username and password.

#### 7. Start the Server

Run the development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
```

Open your browser and go to **http://localhost:8000/** to access Scrapple!

## Usage

### Creating a Search

1. Go to the **Searches** page (link in the navigation)
2. Enter a title for your search (e.g., "Python Tips")
3. Enter search terms separated by commas (e.g., `python, tutorial`)
4. Click **Create Search**

### Running a Scrape

1. On the Searches page, click the search you want to scrape
2. Configure scraping options:
   - **Search Terms**: What to look for
   - **Subreddit**: Leave blank to search all of Reddit, or enter a specific subreddit (e.g., `python`)
   - **Limit**: How many posts to retrieve (default: 100)
   - **Include NSFW**: Check if you want adult content included
   - **Sort**: Choose `new`, `top`, `relevance`, etc.
3. Click **Scrape** to fetch results

### Browsing Results

- The **Feed** page shows all scraped posts
- Use the dropdown to filter by a specific search
- Click on post titles to view them on Reddit
- Posts are paginated (25 per page)

### API Access

If you're a developer, you can use the REST API:

```bash
# Get all searches
curl http://localhost:8000/api/searches/

# Create a new search
curl -X POST http://localhost:8000/api/searches/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My Search", "search_terms": ["term1", "term2"]}'

# Run a scrape
curl -X POST http://localhost:8000/api/scrape/ \
  -H "Content-Type: application/json" \
  -d '{
    "search_id": 1,
    "search_terms": ["python"],
    "subreddit": "python",
    "limit": 50
  }'
```

## Configuration

The main configuration file is `scrapple/settings.py`. Most users won't need to change anything, but here are some common tweaks:

- **Database**: Change `DATABASES` to use PostgreSQL or another database
- **Allowed Hosts**: If hosting on a domain, update `ALLOWED_HOSTS`
- **Debug Mode**: Set `DEBUG = False` in production

## Troubleshooting

**"Python not found"**: Make sure Python is installed and in your PATH. Try `python --version` or `python3 --version`.

**"ModuleNotFoundError"**: Make sure your virtual environment is activated (you should see `(venv)` in your terminal).

**"Port 8000 already in use"**: Another process is using port 8000. Either stop it or run: `python manage.py runserver 8001`

**Scrapes aren't returning results**: Reddit may be blocking requests. Check your internet connection or try a different search term.

## Production Deployment

For production use:

1. Set `DEBUG = False` in `scrapple/settings.py`
2. Set a strong `SECRET_KEY` (use a tool like `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
3. Consider using a production database like PostgreSQL
4. Use a production ASGI server like Gunicorn or uWSGI
5. Set up a reverse proxy (Nginx) to handle static files and SSL

For detailed deployment instructions, see [Django's deployment guide](https://docs.djangoproject.com/en/4.2/howto/deployment/).

## License

This project is licensed under the **MIT License**, which means:
- You can use, modify, and distribute this code freely
- You can fork your own version and make it your own
- You can use it for personal or commercial projects
- The only requirement is to include the original license notice

See [LICENSE](LICENSE) for details.