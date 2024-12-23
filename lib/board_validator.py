from lib.checkers import is_content_scrapeable
from lib.file_manager import FileManager

class BoardValidator:
    def __init__(self, max_retry_limit=3):
        self.fm = FileManager()
        self.MAX_RETRY_LIMIT = max_retry_limit
        
    
    def get_valid_job_boards(self):
        valid_list = list(filter(self.is_job_board_valid, self.fm.job_boards))
        print(f"====== REMOVED INVALID JOB BOARDS ======")
        return valid_list
    
    def is_job_board_valid(self, job_board_url):
        if self.is_below_retry_limit(job_board_url) and is_content_scrapeable(job_board_url):
            return True
        
        print(f"INVALID JOB BOARD: {job_board_url}")
        self.add_unparsable_board(job_board_url)
        return False

    def is_below_retry_limit(self, job_board_url):
        # if the current job board exceeds the give retry amount, we stop parsing it.
        for job in self.fm.unparsed_job_boards:
            if job_board_url in job:
                if job[job_board_url] >= self.MAX_RETRY_LIMIT: 
                    print(f"Skipping previously identified unparseable board: {job_board_url}")
                    return False
        return True

    def add_unparsable_board(self, job_board_url):
        if job_board_url not in self.fm.unparsed_job_boards:
            new_board = {
                "url": job_board_url,
                "failure_count": 0,
                "failure_reason": "wow"
            }
            self.fm.unparsed_job_boards.append(new_board)
        else:
            self.fm.increment_job_board_fail_count(job_board_url)
