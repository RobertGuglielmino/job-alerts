import asyncio
from datetime import date, timedelta
import traceback
from lib.file_manager import FileManager
from lib.job_notifier import JobNotifier
# https://medium.com/@beckernick/faster-web-scraping-in-python-e3fba2ebb541


# LINKEDIN SCRAPER
# https://github.com/jwc20/linkedin-scraper-jobs/tree/main

# WAASU SCRAPER
# https://github.com/jwc20/waasuapi/tree/main 

# WELLFOUND SCRAPER
# https://github.com/jwc20/wellfound-scraper

async def check_job_boards():
    notifier = JobNotifier()
    await notifier.check_job_boards()  # Your original check function

async def schedule_periodic():
    while True:
        try:
            await check_job_boards()
        except Exception as e:
            print(f"Error in check_job_boards: {traceback.format_exc()}")
            # You might want to add logging here
        
        # Wait for 1 hour
        await asyncio.sleep(3600)  # 3600 seconds = 1 hour
        
async def main():

    # # clean up listings older than 30 days on startup
    # fm = FileManager()
    # fm.clean_up_old_openings()

    # Start the periodic task
    await schedule_periodic()

if __name__ == "__main__":
    asyncio.run(main())