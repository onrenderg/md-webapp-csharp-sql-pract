# I have multiple URLs that I want to convert to PDF in that sequence from list of urls named url_list 

# pip install pdfkit using wkhtmltopdf 

import pdfkit 
import requests
import time

# List of URLs to convert to PDF (using a smaller test set first)
url_list = [
    "https://www.guru99.com/c-sharp-tutorial.html",
    "https://www.guru99.com/net-framework.html",
    "https://www.guru99.com/c-sharp-dot-net-version-history.html",
    "https://www.guru99.com/download-install-visual-studio.html",
    "https://www.guru99.com/c-sharp-fundamentals-arrays-enumeration.html",
    "https://www.guru99.com/c-sharp-data-types.html",
    "https://www.guru99.com/c-sharp-enum.html",
    "https://www.guru99.com/c-sharp-variables-operator.html",
    "https://www.guru99.com/c-sharp-conditional-statements.html",
    "https://www.guru99.com/c-sharp-arrays.html",
    "https://www.guru99.com/c-sharp-class-object.html",
    "https://www.guru99.com/c-sharp-class-object.html",
    "https://www.guru99.com/c-sharp-access-modifiers-constructor.html",
    "https://www.guru99.com/c-sharp-inheritance-polymorphism.html",
    "https://www.guru99.com/c-sharp-abstract-class.html",
    "https://www.guru99.com/c-sharp-interface.html",
    "https://www.guru99.com/c-sharp-collections.html",
    "https://www.guru99.com/c-sharp-arraylist.html",
    "https://www.guru99.com/c-sharp-stack.html",
    "https://www.guru99.com/c-sharp-queue.html",
    "https://www.guru99.com/c-sharp-hashtable.html",
    "https://www.guru99.com/c-sharp-windows-forms-application.html",
    "https://www.guru99.com/c-sharp-access-database.html",
    "https://www.guru99.com/c-sharp-file-operations.html",
    "https://www.guru99.com/c-sharp-stream.html",
    "https://www.guru99.com/c-sharp-serialization.html",
    "https://www.guru99.com/coded-ui-test-cuit.html",
    "https://www.guru99.com/c-sharp-interview-questions.html",
     "https://www.guru99.com/c-sharp-serialization.html",
     "https://www.guru99.com/coded-ui-test-cuit.html",
     "https://www.guru99.com/c-sharp-interview-questions.html"
]

path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
output_path = 'combined_pages.pdf'

# Options to handle network issues and improve compatibility
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in', 
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None,
    'enable-local-file-access': None,
    'load-error-handling': 'ignore',
    'load-media-error-handling': 'ignore',
    'javascript-delay': 1000  # Wait for JS to load
}

config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

# Test connectivity to URLs first
print("Testing connectivity to URLs...")
valid_urls = []
for i, url in enumerate(url_list, 1):
    try:
        print(f"[{i}/{len(url_list)}] Testing {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        valid_urls.append(url)
        print(f"  ✓ Accessible")
        time.sleep(1)  # Be respectful to the server
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Failed: {e}")
        continue

if not valid_urls:
    print("✗ No accessible URLs found. Please check your internet connection.")
    exit(1)

print(f"\nFound {len(valid_urls)} accessible URLs out of {len(url_list)}")

# Generate PDF from valid URLs
try:
    print("\nGenerating combined PDF...")
    pdfkit.from_url(valid_urls, output_path, options=options, configuration=config)
    print(f"✓ PDF created successfully: {output_path}")
    print(f"Combined {len(valid_urls)} pages into the PDF")
except Exception as e:
    print(f"✗ Error creating PDF: {e}")
    print("Make sure wkhtmltopdf is installed correctly.")
