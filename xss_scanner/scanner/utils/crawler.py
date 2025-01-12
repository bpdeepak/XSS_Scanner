import requests
from bs4 import BeautifulSoup

def crawl_url(url):
    """
    Crawls a given URL to find input fields.
    :param url: The target URL to scan.
    :return: A list of form action URLs and their input fields.
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract forms and their input fields
        forms = soup.find_all('form')
        form_data = []
        for form in forms:
            action = form.get('action', url)  # Default to current URL if action is not specified
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])
            form_data.append({
                'action': action,
                'method': method,
                'inputs': inputs
            })
        return form_data
    except Exception as e:
        print(f"Error crawling URL {url}: {e}")
        return []
