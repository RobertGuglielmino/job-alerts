from bs4 import BeautifulSoup
import requests
import re

def detect_nextjs_and_pagination(url: str) -> bool:
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        html_content = response.text
        
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for NextJS
        has_nextjs = _detect_nextjs(soup)
        
        # Check for pagination
        has_pagination = _detect_pagination(soup)
        
        return has_nextjs and has_pagination
    
    except Exception as e:
        print(f"Error analyzing webpage: {str(e)}")
        return {
            'is_nextjs': False,
            'has_pagination': False
        }

def _detect_nextjs(soup: BeautifulSoup) -> bool:
    # Check for indicators of client-side rendered content
    critical_indicators = [
        lambda s: bool(s.find('div', {'id': '__next'}, text=re.compile(r'^\s*$'))),
        lambda s: bool(s.find(class_=re.compile(r'loading|skeleton|placeholder|shimmer'))),
        lambda s: bool(s.find(attrs={'aria-hidden': 'true'})) and not bool(s.find('a', recursive=True)),
        lambda s: any(
            container.find('a') is None and 'job' in container.get('class', [''])[0].lower()
            for container in s.find_all(['div', 'section'], class_=re.compile(r'job|listing|position'))
        ),
        lambda s: bool(s.find('script', string=re.compile(r'window\.__NEXT_DATA__.*jobs|positions|listings'))),
        lambda s: bool(s.find('script', string=re.compile(r'"/api/jobs"|"/api/positions"|"/api/listings"'))),
    ]

    # Look for indicators that the job content is statically rendered
    static_indicators = [
        lambda s: bool(s.find('a', href=re.compile(r'job|career|position'))),
        lambda s: bool(s.find(['div', 'section'], class_=re.compile(r'job|listing|position'), text=re.compile(r'\S'))),
    ]

    if any(indicator(soup) for indicator in static_indicators):
        return False

    return any(indicator(soup) for indicator in critical_indicators)


def _detect_pagination(soup: BeautifulSoup) -> bool:
    pagination_indicators = [
        # Class patterns
        lambda s: bool(s.find(class_=re.compile(r'pagination', re.I))),
        lambda s: bool(s.find(class_=re.compile(r'pager', re.I))),
        lambda s: bool(s.find(class_=re.compile(r'pages?', re.I))),
        
        # Role patterns
        lambda s: bool(s.find(attrs={'role': 'navigation'})),
        
        # ARIA patterns
        lambda s: bool(s.find(attrs={'aria-label': re.compile(r'pagination', re.I)})),
        
        # Common navigation patterns
        lambda s: bool(s.find('nav', class_=re.compile(r'pagination|pager|pages?', re.I))),
        
        # Common pagination elements
        lambda s: bool(s.find(class_='page-numbers')),
        lambda s: bool(s.find(attrs={'data-pagination': True})),
        
        # Common link patterns
        lambda s: bool(s.find_all('a', href=re.compile(r'[?&]page=\d+'))),
        lambda s: bool(s.find_all('a', href=re.compile(r'/page/\d+'))),
    ]
    
    return any(indicator(soup) for indicator in pagination_indicators)