import asyncio
from lib.job_notifier import JobNotifier
# https://medium.com/@beckernick/faster-web-scraping-in-python-e3fba2ebb541


async def check_job_boards():
    notifier = JobNotifier()
    await notifier.check_job_boards()  # Your original check function

async def schedule_periodic():
    while True:
        try:
            await check_job_boards()
        except Exception as e:
            print(f"Error in check_job_boards: {e}")
            # You might want to add logging here
        
        # Wait for 1 hour
        await asyncio.sleep(3600)  # 3600 seconds = 1 hour
        
async def main():
    # Start the periodic task
    await schedule_periodic()

if __name__ == "__main__":
    asyncio.run(main())