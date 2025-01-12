# Automated XSS Vulnerability Scanner

An **Automated Cross-Site Scripting (XSS) Vulnerability Scanner** built in Python and Django, designed to detect both **reflected XSS** and **stored XSS** vulnerabilities. The project includes a **deliberately vulnerable web application** for testing, which is also built using Django.

---

## Features

1. **XSS Scanner:**

   - Detects **Reflected XSS** vulnerabilities.
   - Detects **Stored XSS** vulnerabilities.
   - Provides actionable fix suggestions for detected vulnerabilities.
   - Simple Django web interface to input target URLs and view scan results.

2. **Vulnerable Web Application:**
   - Demonstrates real-world **Reflected XSS** and **Stored XSS** vulnerabilities.
   - Allows for testing the scanner's effectiveness.

---

## Technologies Used

- **Backend:** Python, Django
- **Web Scraping:** Requests, BeautifulSoup
- **Testing for Dynamic Content (Optional):** Selenium
- **Database:** SQLite (for vulnerable app)
- **Development Environment:** Django development server

---

## Directory Structure

### XSS Scanner

```
xss_scanner/
├── manage.py
├── scanner/
│   ├── migrations/
│   ├── templates/
│   │   ├── scan_form.html
│   │   └── scan_results.html
│   ├── utils/
│   │   ├── crawler.py       # Crawling input fields from forms
│   │   ├── payloads.py      # XSS payloads for testing
│   │   └── scanner.py       # Logic for detecting XSS vulnerabilities
│   ├── views.py             # Handles user requests
│   ├── urls.py              # Routes for the scanner app
├── db.sqlite3               # Scanner database
├── requirements.txt         # Project dependencies
└── settings/
    ├── settings.py          # Django settings
    ├── urls.py              # Project-level routes
```

### Vulnerable Web Application

```
vulnerable_app/
├── manage.py
├── xss_vulnerable/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html         # Base HTML template
│   │   ├── home.html         # Reflected XSS example
│   │   └── comments.html     # Stored XSS example
│   ├── models.py             # Models for comments
│   ├── views.py              # Handles vulnerable endpoints
│   ├── urls.py               # Routes for the vulnerable app
├── db.sqlite3                # Vulnerable app database
└── requirements.txt          # Project dependencies
```

---

## Setup Instructions

### 1. Set Up the Vulnerable Web Application

1. Navigate to the `vulnerable_app` directory:
   ```bash
   cd vulnerable_app
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the server on port `8001`:
   ```bash
   python manage.py runserver 8001
   ```
5. Access the vulnerable app at `http://127.0.0.1:8001/`.

---

### 2. Set Up the XSS Scanner

1. Navigate to the `xss_scanner` directory:
   ```bash
   cd xss_scanner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server on port `8000`:
   ```bash
   python manage.py runserver
   ```
4. Access the scanner at `http://127.0.0.1:8000/`.

---

## Usage

### 1. Using the Vulnerable App

- Visit `http://127.0.0.1:8001/`:
  - Test **Reflected XSS** on the **Search** page.
  - Test **Stored XSS** on the **Comments** page.

### 2. Scanning the Vulnerable App

- Visit `http://127.0.0.1:8000/`:
  - Enter `http://127.0.0.1:8001/` as the target URL.
  - Click "Scan" to identify vulnerabilities in the vulnerable app.
  - View results with vulnerability type (Reflected or Stored XSS) and fix suggestions.

---

## Example Output

### Scanner Results

```
Input Field: username | Payload: <script>alert('XSS')</script> | Vulnerable: True | Type: Stored XSS
Input Field: query | Payload: <img src=x onerror=alert('XSS')> | Vulnerable: True | Type: Reflected XSS
```

---

## Next Steps

1. **Enhancements for Scanner:**

   - Add support for **DOM-based XSS** using Selenium.
   - Generate detailed reports in JSON or HTML format.
   - Handle authenticated areas by implementing login functionality.

2. **Enhancements for Vulnerable App:**
   - Add more input fields and endpoints with other types of vulnerabilities.
   - Implement file uploads or AJAX-based inputs for broader testing scenarios.

---

## Dependencies

Install the following dependencies for both the scanner and the vulnerable app:

```
Django==3.x
requests
beautifulsoup4
selenium  # Optional, for dynamic content testing
```

---

## Contributing

Feel free to fork this project, submit issues, or suggest improvements. Contributions are welcome!

---

## License

This project is licensed under the MIT License.

```

```
