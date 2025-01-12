from django.shortcuts import render
from .utils.crawler import crawl_url
from .utils.scanner import detect_xss
from .utils.payloads import xss_payloads
from .utils.reports import save_scan_results


def scan(request):
    """
    Handles XSS scanning requests.
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        forms = crawl_url(url)
        results = detect_xss(url, forms, xss_payloads)
        
        # Generate reports
        save_scan_results(results)
        
        return render(request, 'scan_results.html', {'results': results})
    return render(request, 'scan_form.html')