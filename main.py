import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import logging


class Job:
    """
    Represents a job listing with title, company, location, and description.
    """

    def __init__(self, title: str, company: str, location: str, description: str):
        self.title = title
        self.company = company
        self.location = location
        self.description = description


class JobScraper:
    """
    Scrapes job listings from a given URL.
    """

    def __init__(self, url: str):
        self.url = url

    def scrape_job_listings(self) -> list[Job]:
        """
        Scrapes job listings from a given URL and returns a list of Job objects.
        """
        try:
            response = requests.get(self.url)
            soup = BeautifulSoup(response.text, "html.parser")
            job_listings = soup.find_all("div", class_="job-listing")

            job_details = []

            for job_listing in job_listings:
                title = job_listing.find("h2").text.strip()
                company = job_listing.find("p", class_="company").text.strip()
                location = job_listing.find(
                    "p", class_="location").text.strip()
                description = job_listing.find(
                    "div", class_="description").text.strip()

                job = Job(title, company, location, description)
                job_details.append(job)

            return job_details

        except requests.exceptions.RequestException as e:
            logging.error(f"Error occurred during scraping: {e}")
            return []

    def run(self):
        """
        Runs the job scraper and starts the Flask app.
        """
        app = Flask(__name__)
        job_scraper = JobScraper("https://www.example.com/job-listings")

        @app.route("/")
        def home():
            """
            Renders the home page.
            """
            return render_template("index.html")

        @app.route("/job_listings")
        def job_listings():
            """
            Renders the job listings page with scraped job details.
            """
            job_details = job_scraper.scrape_job_listings()
            return render_template("job_listings.html", job_details=job_details)

        try:
            app.run()
        except Exception as e:
            logging.error(f"Error occurred during app execution: {e}")


if __name__ == "__main__":
    scraper = JobScraper("https://www.example.com/job-listings")
    scraper.run()
