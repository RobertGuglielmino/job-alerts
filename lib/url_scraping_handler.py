from datetime import date
from typing import Dict, List

from bs4 import BeautifulSoup
from lib.file_manager import FileManager
from lib.helpers import _detect_pagination_pattern, _get_next_page_url
from playwright.async_api import async_playwright


class URLScraper:
    def __init__(self):
        self.fm = FileManager()
        self.current_session_jobs = set()
        self.max_pages = 5


    async def get_board_html_as_page_strings(self, url: str) -> List[Dict[str, str]]:
        all_scraped_html = []
        pages_scraped = 0
        current_url = url
        
        async with async_playwright() as p:
            try:
                # set up web scraping
                browser = await p.chromium.launch()
                context = await browser.new_context()
                page = await context.new_page()
                pattern = None

                while pages_scraped < self.max_pages and current_url:
                    # scrape html
                    content = await self._scrape_url_for_html_rendered(page, current_url)
                    # if pattern != None:
                    pattern = _detect_pagination_pattern(current_url, content)
                    all_scraped_html.append({
                        "url": current_url,
                        "content": content
                    })
                        
                    # go to next page
                    current_url = _get_next_page_url(pattern, content)
                    pages_scraped += 1
                        
            except Exception as e:
                print(f"ERROR scraping url to an HTML String {url}: {str(e)}")
            finally:
                await browser.close()
        
        return all_scraped_html

    async def _scrape_url_for_html_rendered(self, page, url: str) -> str:
        """Get fully rendered page content including JavaScript-generated elements."""
        try:
            # Wait for network idle to ensure dynamic content is loaded
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_load_state('domcontentloaded')
            
            # Additional wait for dynamic content
            try:
                # Wait for any of these common selectors
                await page.wait_for_selector([
                    '[class*="job"]',
                    '[class*="a"]',
                    '[class*="position"]',
                    '[class*="listing"]',
                    '[class*="vacancy"]'
                ], timeout=5000)
            except:
                # Continue if timeout - page might not have these specific selectors
                pass

            # Get computed styles and pseudo-elements
            content = await page.evaluate('''() => {
                function getPseudoContent(element, pseudo) {
                    const style = window.getComputedStyle(element, pseudo);
                    return style.getPropertyValue('content');
                }
                
                function getElementContent(element) {
                    let content = element.textContent || '';
                    
                    // Get ::before content
                    const beforeContent = getPseudoContent(element, ':before');
                    if (beforeContent && beforeContent !== 'none') {
                        content = beforeContent.replace(/['"]/g, '') + content;
                    }
                    
                    // Get ::after content
                    const afterContent = getPseudoContent(element, ':after');
                    if (afterContent && afterContent !== 'none') {
                        content = content + afterContent.replace(/['"]/g, '');
                    }
                    
                    return content;
                }
                
                // Process all elements
                const elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    const fullContent = getElementContent(el);
                    if (fullContent !== el.textContent) {
                        // Create a new text node with the full content
                        el.textContent = fullContent;
                    }
                });
                
                return document.documentElement.outerHTML;
            }''')
            
            return content
            
        except Exception as e:
            print(f"Error rendering {url}: {str(e)}")
            return ""

    def scraped_html_to_job_openings(self, boards_as_str):
        all_jobs = []
        for board in boards_as_str:
            all_jobs.extend(self.scrape_board_for_openings(board))
            
        print(f"====== SCRAPED HTML FOR JOB OPENINGS ======")
        return all_jobs
    
    def scrape_board_for_openings(self, board) -> List[Dict[str, str]]:
        soup_page = BeautifulSoup(board['content'], 'html.parser')
        url = board['url']

        try:
            jobs = []
            page_jobs = set()

            for job in soup_page.find_all(['a']):  # Common job container tags
                # Extract job title from any nested tag
                job_title = job.get_text(strip=True)

                job_key = f"{job_title}_{job.get('href', '')}"
                if job_key in self.current_session_jobs:
                    continue

                if job and job_title and self.fm._matches_criteria(job_title):
                    print(f"MATCHED JOB TITLE {job_title}")
                    href = job['href']
                    if not href.startswith('http'):
                        # Handle relative URLs
                        href = f"{url.rstrip('/')}/{href.lstrip('/')}"
                    
                    if job_key not in page_jobs:
                        jobs.append({
                            'title': job_title,
                            'url': href,
                            'date_added': date.today()
                        })
                        page_jobs.add(job_key)
                        self.current_session_jobs.add(job_key)
            
            return jobs
        except Exception as e:
            print(f"Error reading openings from html at {url}: {str(e)}")
            return []
        