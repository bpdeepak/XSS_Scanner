import json
import logging

# Configure logging for the scanner
logging.basicConfig(
    filename="scanner_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def generate_json_report(results, output_file="scan_report.json"):
    """
    Generates a JSON report for the scan results.
    :param results: List of scan results.
    :param output_file: Name of the JSON report file.
    """
    with open(output_file, 'w') as file:
        json.dump(results, file, indent=4)
    logging.info(f"JSON report generated: {output_file}")
    print(f"JSON report generated: {output_file}")


def sanitize_html(input_string):
    """
    Escapes special characters in a string to prevent XSS in the HTML report.
    :param input_string: The string to sanitize.
    :return: Sanitized string.
    """
    return (
        input_string.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def generate_html_report(results, output_file="scan_report.html"):
    """
    Generates an HTML report for the scan results.
    :param results: List of scan results.
    :param output_file: Name of the HTML report file.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>XSS Scanner Report</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f4f4f4; }
        </style>
    </head>
    <body>
        <h1>XSS Scanner Report</h1>
        <table>
            <thead>
                <tr>
                    <th>Payload</th>
                    <th>Type</th>
                    <th>Vulnerability</th>
                    <th>Fix Suggestion</th>
                </tr>
            </thead>
            <tbody>
    """
    for result in results:
        sanitized_payload = sanitize_html(result['payload'])  # Sanitize the payload
        sanitized_fix_suggestion = sanitize_html(result['fix_suggestion'])  # Sanitize the fix suggestion
        html_content += f"""
            <tr>
                <td>{sanitized_payload}</td>
                <td>{result['type']}</td>
                <td>{'Yes' if result['vulnerability'] else 'No'}</td>
                <td>{sanitized_fix_suggestion}</td>
            </tr>
        """
    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Write the HTML content to a file
    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML report generated: {output_file}")



def save_scan_results(results):
    """
    Saves the scan results to JSON and HTML files and prints a summary to the terminal.
    :param results: List of scan results.
    """
    # Save JSON and HTML reports
    generate_json_report(results, "scanner_reports/scan_report.json")
    generate_html_report(results, "scanner_reports/scan_report.html")
    
    # Generate a concise summary
    total_tests = len(results)
    vulnerable_tests = sum(1 for result in results if result['vulnerability'])
    
    # Log summary
    logging.info(f"Total payloads tested: {total_tests}")
    logging.info(f"Vulnerabilities found: {vulnerable_tests}")
    
    # Print summary to terminal
    print(f"\n--- Scan Summary ---")
    print(f"Total payloads tested: {total_tests}")
    print(f"Vulnerabilities found: {vulnerable_tests}")
    print(f"Detailed results saved in 'scanner_reports/scan_report.json' and 'scanner_reports/scan_report.html'.")
