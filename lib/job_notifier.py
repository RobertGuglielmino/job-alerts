from lib.file_manager import FileManager
from lib.board_validator import BoardValidator
from lib.url_scraping_handler import URLScraper
from notifiers import format_jobs_email

class JobNotifier:
    def __init__(self):
        self.max_pages = 100
        self.fm = FileManager()

        self.board_validator = BoardValidator()
        self.url_scraper = URLScraper()


    async def check_job_boards(self):
        new_jobs = []
        scraped_html_pages = []

        valid_job_boards = self.board_validator.get_valid_job_boards()

        for board in valid_job_boards:
            scraped_html_pages.extend(await self.url_scraper.get_board_html_as_page_strings(board))
        print(f"====== PARSED HTML FROM JOB BOARDS ======")

        openings_from_html = self.url_scraper.scraped_html_to_job_openings(scraped_html_pages)
        

        for opening in openings_from_html:
            opening_key = f"{opening['title']}_{opening['url']}"
            if opening_key not in self.fm.jobs_seen:
                print(f"New job found: {opening['title']}")
                new_jobs.append(opening)
                self.fm.jobs_seen.add(opening_key)
        

        format_jobs_email(new_jobs)

        self.fm._save_unparsed_job_boards()
        self.fm._save_jobs_seen()

        print(f"COMPLETED this round of job alerts.")

