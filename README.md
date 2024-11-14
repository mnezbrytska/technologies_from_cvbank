# Python Job Scraper

This project scrapes Python job listings from CVBankas, extracting job titles, companies, locations, salaries, and descriptions. It also analyzes technology demand within these listings.

## Requirements

Install dependencies:
```bash
pip install pandas requests beautifulsoup4 selenium matplotlib
```

## Setup

1. **WebDriver**: Download and install the [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).
2. **Libraries**: The script uses `pandas`, `requests`, `BeautifulSoup` (from `bs4`), `selenium`, and `matplotlib`.

## How It Works

1. **Fetch Vacancy Links**: Collects job URLs for Python listings on CVBankas.
2. **Parse Job Data**: Extracts title, company, location, salary, and description.
3. **Save to CSV**: Job details are saved in `cvbankas_python_vacancies.csv`.
4. **Technology Analysis**:
   - Searches for key technologies in descriptions and saves counts in `tech_demand_counts.csv`.
5. **Visualization**: Generates a bar chart showing technology demand.

## Key Functions

- `fetch_vacancy_links()`: Collects all job URLs.
- `parse_vacancy(url)`: Extracts job details from each page.
- `scrape_cvbankas()`: Scrapes all listings and saves to CSV.
- `get_job_description(url)`: Fetches job descriptions for tech analysis.

## Usage

Run the script:
```bash
python <script_name>.py
```

### Outputs

- **`cvbankas_python_vacancies.csv`**: Job listings data.
- **`tech_demand_counts.csv`**: Counts of each technology.

This tool provides insight into technology trends for Python roles on CVBankas.