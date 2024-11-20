import json
import os
from typing import List, Set

class FileManager:
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

        
    def _matches_criteria(self, job_title: str) -> bool:
        job_title_lower = job_title.lower()
        
        # Check if job matches any allowed terms
        matches_allow = any(allow_term.lower() in job_title_lower 
                          for allow_term in self.allow_list)
        
        # Check if job matches any blocked terms
        matches_block = any(block_term.lower() in job_title_lower 
                          for block_term in self.block_list)
        
        return matches_allow and not matches_block

    def _load_jobs_seen(self) -> Set[str]:
        if os.path.exists(self.jobs_seen_file):
            with open(self.jobs_seen_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def _load_unparsed_job_boards(self) -> Set[str]:
        if os.path.exists(self.unparsed_job_boards_file):
            with open(self.unparsed_job_boards_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_jobs_seen(self):
        with open(self.jobs_seen_file, 'w') as f:
            json.dump(list(self.jobs_seen), f)

    def _save_unparsed_job_boards(self):
        with open(self.unparsed_job_boards_file, 'w') as f:
            json.dump(list(self.unparsed_job_boards), f)

    def _load_file_lines(self, filename: str) -> List[str]:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return [line.strip() for line in f if line.strip()]
        return []
