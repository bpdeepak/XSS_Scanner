from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, WebDriverException, NoSuchElementException
import requests, time, logging

# Configure logging
logging.basicConfig(
    filename='scanner_logs.log',  # Log output to a file
    level=logging.INFO,           # Set log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_fix_suggestion(payload):
    payload_suggestions = {
        "<script>alert('XSS')</script>": "Escape angle brackets (<, >) in user inputs using a server-side escaping library.",
        "<img src=x onerror=alert('XSS')>": "Validate image sources and disallow untrusted domains.",
        "<svg/onload=alert('XSS')>": "Sanitize SVG content or use tools like DOMPurify to remove scripts.",
        "<b onmouseover=alert('XSS')>Hover me!</b>": "Strip event handler attributes like onmouseover from user inputs.",
        "';alert('XSS');//": "Escape single quotes, double quotes, and semicolons in user inputs.",
        "<script>document.write(document.cookie)</script>": "Avoid using document.write or sanitize its input rigorously.",
        "javascript:alert('XSS')": "Disallow javascript: URIs in links or attributes.",
        "'\"><script>alert(1)</script>": "Escape quotes and angle brackets in user inputs.",
        "<iframe src='javascript:alert(`XSS`)'></iframe>": "Restrict iframe sources to trusted domains.",
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */onerror=alert(1))//%0D%0A%0d%0a//</style></title></textarea></noscript>": "Sanitize all user inputs and validate URIs to disallow javascript schemes.",
        "<button onclick=alert(1)>Click Me</button>": "Remove event handler attributes like onclick from user inputs.",
        "<svg><script>alert(1)</script></svg>": "Disallow SVG content with embedded scripts.",
        "<sCriPt>alert('XSS')</sCriPt>": "Normalize inputs to lowercase and then sanitize to prevent bypasses.",
        "<a href=javascript:alert('XSS')>Click Here</a>": "Disallow javascript: URIs in hyperlinks.",
        "<input type='text' onfocus=alert('XSS') autofocus>": "Strip event handler attributes like onfocus.",
        "<details open ontoggle=alert('XSS')>Hover me!</details>": "Disallow or sanitize HTML5-specific attributes like ontoggle.",
        "<video src=x onerror=alert('XSS')></video>": "Validate video sources and sanitize attributes.",
        "<object data='javascript:alert(`XSS`)'></object>": "Disallow or sanitize object data attributes.",
        "<embed src='javascript:alert(`XSS`)'>": "Restrict embed sources to trusted domains.",
        "<body onload=alert('XSS')>": "Remove or sanitize onload and other body event handlers.",
        "https://example.com/path?param=<script>alert('XSS')</script>": "Sanitize URL query parameters to disallow script injection.",
        "https://example.com/#<script>alert('XSS')</script>": "Sanitize fragment identifiers (#) in URLs.",
        "<svg><style>{-o-link-source:expression(alert(1))}</style></svg>": "Disable CSS expressions and sanitize inline styles.",
        "<img src=`javascript:alert(\"XSS\")`>": "Validate image sources and disallow JavaScript URIs.",
        "<iframe srcdoc=\"<script>alert(1)</script>\"></iframe>": "Sanitize iframe srcdoc content.",
        "<script>alert(String.fromCharCode(88,83,83))</script>": "Sanitize dynamically generated scripts to disallow malicious input.",
        "%3Cscript%3Ealert%28'XSS'%29%3C%2Fscript%3E": "Decode URL-encoded inputs before sanitization.",
        "&#x3C;script&#x3E;alert('XSS')&#x3C;/script&#x3E;": "Decode HTML entities and sanitize the decoded input."
    }
    return payload_suggestions.get(payload, "General advice: Sanitize and validate all user inputs rigorously before rendering.")



def detect_dom_xss(base_url, payloads):
    """
    Detects DOM-based XSS vulnerabilities using Selenium and handles alerts gracefully.
    """
    results = []
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and configured

    try:
        for payload in payloads:
            test_url = f"{base_url.rstrip('/')}/dom-xss?input={payload}"
            logging.info(f"Testing URL: {test_url}")
            
            try:
                driver.get(test_url)
                time.sleep(2)  # Wait for the page to load

                # Handle alerts
                try:
                    alert = Alert(driver)
                    alert_text = alert.text
                    alert.accept()
                    logging.info(f"Alert detected and dismissed: {alert_text}")

                    results.append({
                        'url': test_url,
                        'payload': payload,
                        'vulnerability': True,
                        'type': 'DOM-based XSS',
                        'alert_text': alert_text,
                        'fix_suggestion': get_fix_suggestion(payload)
                    })
                except NoAlertPresentException:
                    logging.info("No alert detected.")

                # Check DOM for payload rendering
                try:
                    output_element = driver.find_element(By.ID, 'output')
                    if payload in output_element.get_attribute('innerHTML'):
                        results.append({
                            'url': test_url,
                            'payload': payload,
                            'vulnerability': True,
                            'type': 'DOM-based XSS',
                            'fix_suggestion': get_fix_suggestion(payload)
                        })
                except NoSuchElementException:
                    logging.warning(f"No output element found for {test_url}")
            
            except UnexpectedAlertPresentException as e:
                logging.error(f"Unexpected alert detected: {e}")
    finally:
        driver.quit()

    return results



def detect_xss(url, forms, payloads):
    """
    Detects both reflected and stored XSS by submitting payloads and checking for vulnerabilities.
    :param url: Base URL of the target.
    :param forms: List of forms with input fields.
    :param payloads: List of XSS payloads.
    :return: List of detected XSS vulnerabilities (both reflected and stored).
    """
    results = []
    session = requests.Session()  # Use a session for consistent cookies and headers

    for payload in payloads:
        for form in forms:
            # Prepare form action URL
            action_url = form['action'] if form['action'].startswith('http') else f"{url.rstrip('/')}/{form['action'].lstrip('/')}"
            method = form['method']
            inputs = form['inputs']

            # Prepare form data with the payload
            data = {}
            for input_field in inputs:
                input_name = input_field.get('name')
                if not input_name:
                    continue
                data[input_name] = payload

            try:
                # Submit the form
                if method == 'post':
                    response = session.post(action_url, data=data, timeout=10)
                else:
                    response = session.get(action_url, params=data, timeout=10)

                # Check for reflected XSS in the immediate response
                if payload in response.text:
                    results.append({
                        'action_url': action_url,
                        'payload': payload,
                        'vulnerability': True,
                        'type': 'Reflected XSS',
                        'fix_suggestion': get_fix_suggestion(payload)
                    })

                # Check for stored XSS by revisiting the base URL or another endpoint
                revisit_response = session.get(url, timeout=10)
                if payload in revisit_response.text:
                    results.append({
                        'action_url': action_url,
                        'payload': payload,
                        'vulnerability': True,
                        'type': 'Stored XSS',
                        'fix_suggestion': get_fix_suggestion(payload)
                    })
            except Exception as e:
                print(f"Error injecting payload to {action_url}: {e}")

    # Test DOM-based XSS
    dom_results = detect_dom_xss(f"{url}", payloads)
    results.extend(dom_results)

    return results
