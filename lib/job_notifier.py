
from typing import Dict, List
from bs4 import BeautifulSoup
from lib.checkers import _detect_nextjs, detect_nextjs_and_pagination
from lib.file_manager import FileManager
from lib.helpers import _detect_pagination_pattern, _get_next_page_url, getUrl
from notifiers import format_jobs_email, format_string_email, send_email
from playwright.async_api import async_playwright

class JobNotifier:
    def __init__(self):
        self.max_pages = 100
        self.fm = FileManager()
        self.current_session_jobs = set()

    def scrape_single_page(self, url: str, soup_page: BeautifulSoup) -> List[Dict[str, str]]:
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
                            'url': href
                        })
                        page_jobs.add(job_key)
                        self.current_session_jobs.add(job_key)
            
            return jobs
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []
        
    async def _scrape_single_page_rendered(self, page, url: str) -> str:
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

    async def check_single_job_board(self, url: str) -> List[Dict[str, str]]:
        """Scrape job listings from all pages."""
        all_jobs = []
        pages_scraped = 0
        current_url = url
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            try:
                # Get initial page
                response = getUrl(current_url)
                
                # Detect pagination pattern
                pattern = _detect_pagination_pattern(current_url, response.text)
                
                content = ""
                soup = BeautifulSoup(response.text, 'html.parser')
                if _detect_nextjs(soup):
                    content = await self._scrape_single_page_rendered(page, current_url)
                else:
                    content = response.text

                soup = BeautifulSoup(content, 'html.parser')

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
                        response = getUrl(next_url)
                        
                        current_url = next_url
                        pages_scraped += 1
                        
                        # Break if no new jobs found (assuming end of listings)
                        if not jobs:
                            break
                        
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
            finally:
                await browser.close()
        
        return all_jobs

    async def check_job_boards(self):
        # print(f"JOB BOARD {self.fm.job_boards}")
        new_jobs = []
        new_unparsed_boards = []
        

        for url in self.fm.job_boards:
            print(f"Job Board Link: {url}")

            if url in self.fm.unparsed_job_boards:
                print(f"Skipping previously identified unparseable board: {url}")
                continue

            if detect_nextjs_and_pagination(url):
                JOB_BOARD_ISSUES = f"{url} has both generated content and pagination. This app doesn't have the capabilities (yet) to read the following pages, so you will still have to manually check the listed job board."
                format_string_email(JOB_BOARD_ISSUES)
                if url not in self.fm.unparsed_job_boards:
                    new_unparsed_boards.append(url)
                    self.fm.unparsed_job_boards.add(url)
                continue
            
            jobs = await self.check_single_job_board(url)
            
            for job in jobs:
                print(f"Job Description {job}")
                job_key = f"{job['title']}_{job['url']}"
                if job_key not in self.fm.jobs_seen:
                    print(f"New job found: {job['title']}")
                    new_jobs.append(job)
                    self.fm.jobs_seen.add(job_key)
            print(f"===============")
        
        try:
            if new_jobs:
                format_jobs_email(new_jobs)
                self.fm._save_jobs_seen()
                print(f"Saved {len(new_jobs)} new jobs")
            
            if new_unparsed_boards:
                self.fm._save_unparsed_job_boards()
                print(f"Saved {len(new_unparsed_boards)} new unparseable boards")
        except Exception as e:
            print(f"Error saving data: {str(e)}")
