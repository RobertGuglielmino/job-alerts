
from dataclasses import dataclass
import re
import time
from typing import Counter, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urljoin, urlparse, urlunparse
from bs4 import BeautifulSoup
import requests

@dataclass
class PaginationPattern:
    url: str
    type: str  # 'query_param', 'path_segment', 'button'
    param_name: Optional[str] = None
    current_page: int = 1

def scrape_job_board(self, url: str) -> List[Dict[str, str]]:
    """Scrape job listings from all pages."""
    all_jobs = []
    pages_scraped = 0
    current_url = url

    print(f"searching {url}")
    
    try:
        # Get initial page
        response = getUrl(current_url, self.headers)
        
        # Detect pagination pattern
        pattern = _detect_pagination_pattern(current_url, response.text)
        soup = BeautifulSoup(response.text, 'html.parser')

        if not pattern:
            jobs = self.scrape_single_page(current_url, soup)
            all_jobs.extend(jobs)
        else:
            while pages_scraped < self.max_pages:
                # Extract jobs from current page
                jobs = self.scrape_single_page(current_url, soup)
                all_jobs.extend(jobs)
                    
                # Get next page URL
                next_url = _get_next_page_url(pattern, response.text)
                if not next_url:
                    break
                    
                # Fetch next page
                response = getUrl(next_url, self.headers)
                
                current_url = next_url
                pages_scraped += 1
                
                # Break if no new jobs found (assuming end of listings)
                if not jobs:
                    break
                
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
    
    return all_jobs

def getUrl(url):
    time.sleep(2)  # Rate limiting
    response = requests.get(url)
    response.raise_for_status()
    return response

def _detect_pagination_pattern(url: str, html: str) -> Optional[PaginationPattern]:
    """Detect the pagination pattern used by the website."""
    soup = BeautifulSoup(html, 'html.parser')
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    pagination_params = ['page', 'p', 'pg', 'offset', 'start']

    # 1. Check for query parameter pagination
    for param in pagination_params:
        if param in query_params:
            return PaginationPattern(url, 'query_param', param)

    # 2. Check for common pagination elements
    pagination_elements = soup.find_all(['a', 'button'], 
        text=re.compile(r'next|forward|›|»|page|^\d+$', re.I))
    
    if pagination_elements:
        # Look for numbered pagination
        page_numbers = []
        for element in pagination_elements:
            if element.name == 'a' and element.get('href'):
                href = element.get('href')
                # Extract potential page numbers from href
                numbers = re.findall(r'/(\d+)(?:/|$)', href)
                page_numbers.extend(numbers)

        if page_numbers:
            # Check if numbers appear in path segments
            most_common_number = Counter(page_numbers).most_common(1)[0][0]
            pattern = f"/{most_common_number}"
            if pattern in url:
                return PaginationPattern(url, 'path_segment')

        # If no path segment pattern found, look for next/forward buttons
        next_buttons = soup.find_all(['a', 'button'], 
            text=re.compile(r'next|forward|›|»', re.I))
        if next_buttons:
            for button in next_buttons:
                if button.name == 'a' and button.get('href'):
                    return PaginationPattern(url, 'button')

    return None


def _get_next_page_url(pattern: PaginationPattern, html: str) -> Optional[str]:
    """Get the URL for the next page based on the detected pattern."""
    if pattern.type == 'query_param':
        parsed_url = urlparse(pattern.url)
        query_params = parse_qs(parsed_url.query)
        
        # Update page parameter
        pattern.current_page += 1
        query_params[pattern.param_name] = [str(pattern.current_page)]
        
        # Reconstruct URL
        new_query = urlencode(query_params, doseq=True)
        parts = list(parsed_url)
        parts[4] = new_query
        return urlunparse(parts)

    elif pattern.type == 'path_segment':
        # Replace or append page number in path
        pattern.current_page += 1
        path_parts = pattern.url.rstrip('/').split('/')
        
        # Try to replace existing page number or append
        page_number_found = False
        for i, part in enumerate(path_parts):
            if part.isdigit():
                path_parts[i] = str(pattern.current_page)
                page_number_found = True
                break
        
        if not page_number_found:
            path_parts.append(str(pattern.current_page))
        
        return '/'.join(path_parts)

    elif pattern.type == 'button':
        soup = BeautifulSoup(html, 'html.parser')
        next_buttons = soup.find_all(['a', 'button'], 
            text=re.compile(r'next|forward|›|»', re.I))
        
        for button in next_buttons:
            if button.name == 'a' and button.get('href'):
                return urljoin(pattern.url, button.get('href'))
        
    return None