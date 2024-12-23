from datetime import date, timedelta
import json
import os
from typing import List

class FileManager():
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(FileManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.unparsed_job_boards_file = "config/unparsed_job_boards_file.json"
        self.jobs_seen_file = "config/jobs_seen.json"
        self.job_boards_file = "config/job_boards.txt"
        self.allow_list_file = "config/allow_list.txt"
        self.block_list_file = "config/block_list.txt"
        self.email_file = "config/email.txt"
        
        # Load persistent data
        self.jobs_seen = self._load_jobs_seen()
        self.job_boards = self._load_file_lines(self.job_boards_file)
        self.allow_list = self._load_file_lines(self.allow_list_file)
        self.block_list = self._load_file_lines(self.block_list_file)
        self.unparsed_job_boards = self._load_unparsed_job_boards()


    def increment_job_board_fail_count(self, url):
        for job_url in self.unparsed_job_boards:
            if url in job_url:
                url['fail_count'] += 1

    def reset_job_board_fail_count(self, url):
        for job_url in self.unparsed_job_boards:
            if url in job_url:
                url['fail_count'] = 0
        
    def _matches_criteria(self, job_title: str) -> bool:
        job_title_lower = job_title.lower()
        
        # Check if job matches any allowed terms
        matches_allow = any(allow_term.lower() in job_title_lower 
                          for allow_term in self.allow_list)
        
        # Check if job matches any blocked terms
        matches_block = any(block_term.lower() in job_title_lower 
                          for block_term in self.block_list)
        
        return matches_allow and not matches_block

    def _load_jobs_seen(self) -> List[str]:
        if os.path.exists(self.jobs_seen_file):
            with open(self.jobs_seen_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _load_unparsed_job_boards(self) -> List[str]:
        if os.path.exists(self.unparsed_job_boards_file):
            with open(self.unparsed_job_boards_file, 'r') as f:
                return list(json.load(f))
        return list()

    def _save_jobs_seen(self):
        try:
            with open(self.jobs_seen_file, 'w') as f:
                json.dump(list(self.jobs_seen), f)
                print(f"Saved new openings")
        except Exception as e:
            print(f"Error saving openings: {str(e)}")

    def _save_unparsed_job_boards(self):
        try:
            with open(self.unparsed_job_boards_file, 'w') as f:
                json.dump(list(self.unparsed_job_boards), f)
                print(f"Saved new unparseable boards")
        except Exception as e:
            print(f"Error saving boards: {str(e)}")

    def _load_file_lines(self, filename: str) -> List[str]:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []


    def clean_up_old_openings(self):
        temp = list(filter(lambda x: x.date_added < date.today() - timedelta(days=30), self.jobs_seen))
        self.jobs_seen = temp
        self._save_jobs_seen()
