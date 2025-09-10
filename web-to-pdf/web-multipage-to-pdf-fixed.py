# Improved multi-page web to PDF converter with better error handling

import pdfkit
import requests
import time
import tempfile
import os

# List of URLs to convert to PDF
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

# More conservative options that are more likely to work
options = {
    'page-size': 'A4',
    'margin-top': '0.75in',
    'margin-right': '0.75in', 
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None,
    'javascript-delay': 2000,  # Wait for JS to load
    'load-error-handling': 'ignore',
    'load-media-error-handling': 'ignore',
    'enable-local-file-access': None,
    'disable-smart-shrinking': None,
    'print-media-type': None
}

config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

def test_connectivity(urls):
    """Test connectivity to URLs and return valid ones"""
    print("Testing connectivity to URLs...")
    valid_urls = []
    for i, url in enumerate(urls, 1):
        try:
            print(f"[{i}/{len(urls)}] Testing {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            valid_urls.append(url)
            print(f"  ✓ Accessible")
            time.sleep(1)  # Be respectful to the server
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed: {e}")
            continue
    return valid_urls

def create_pdf_method1(valid_urls):
    """Method 1: Try to create PDF directly from URLs"""
    try:
        print("\nMethod 1: Generating PDF directly from URLs...")
        pdfkit.from_url(valid_urls, output_path, options=options, configuration=config)
        print(f"✓ PDF created successfully: {output_path}")
        return True
    except Exception as e:
        print(f"✗ Method 1 failed: {e}")
        return False

def create_pdf_method2(valid_urls):
    """Method 2: Create individual PDFs and merge them"""
    try:
        print("\nMethod 2: Creating individual PDFs and combining...")
        temp_pdfs = []
        
        for i, url in enumerate(valid_urls, 1):
            temp_pdf = f"temp_page_{i}.pdf"
            print(f"[{i}/{len(valid_urls)}] Converting {url}...")
            
            try:
                pdfkit.from_url(url, temp_pdf, options=options, configuration=config)
                temp_pdfs.append(temp_pdf)
                print(f"  ✓ Created {temp_pdf}")
                time.sleep(2)  # Give server time between requests
            except Exception as e:
                print(f"  ✗ Failed to create PDF for {url}: {e}")
                continue
        
        if temp_pdfs:
            # Try to merge PDFs (requires PyPDF2 or similar)
            try:
                from PyPDF2 import PdfMerger
                merger = PdfMerger()
                
                for pdf in temp_pdfs:
                    merger.append(pdf)
                
                merger.write(output_path)
                merger.close()
                
                # Clean up temporary files
                for pdf in temp_pdfs:
                    try:
                        os.remove(pdf)
                    except:
                        pass
                
                print(f"✓ Combined PDF created successfully: {output_path}")
                return True
                
            except ImportError:
                print("PyPDF2 not available for merging. Individual PDFs created:")
                for pdf in temp_pdfs:
                    print(f"  - {pdf}")
                return True
                
        else:
            print("✗ No individual PDFs were created successfully")
            return False
            
    except Exception as e:
        print(f"✗ Method 2 failed: {e}")
        return False

def create_pdf_method3(valid_urls):
    """Method 3: Use subprocess to call wkhtmltopdf directly"""
    try:
        import subprocess
        print("\nMethod 3: Using subprocess to call wkhtmltopdf directly...")
        
        # Build command
        cmd = [
            path_to_wkhtmltopdf,
            '--page-size', 'A4',
            '--margin-top', '0.75in',
            '--margin-right', '0.75in',
            '--margin-bottom', '0.75in',
            '--margin-left', '0.75in',
            '--javascript-delay', '2000',
            '--load-error-handling', 'ignore',
            '--load-media-error-handling', 'ignore',
            '--print-media-type'
        ]
        
        # Add URLs
        cmd.extend(valid_urls)
        cmd.append(output_path)
        
        print("Running command:", ' '.join(cmd[:5] + ['...', output_path]))
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✓ PDF created successfully using subprocess: {output_path}")
            return True
        else:
            print(f"✗ Subprocess failed with return code {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Method 3 failed: {e}")
        return False

def main():
    # Remove duplicates while preserving order
    seen = set()
    unique_urls = []
    for url in url_list:
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
    
    print(f"Processing {len(unique_urls)} unique URLs...")
    
    # Test connectivity
    valid_urls = test_connectivity(unique_urls)
    
    if not valid_urls:
        print("✗ No accessible URLs found. Please check your internet connection.")
        return
    
    print(f"\nFound {len(valid_urls)} accessible URLs out of {len(unique_urls)}")
    
    # Try different methods
    methods = [create_pdf_method1, create_pdf_method3, create_pdf_method2]
    
    for method in methods:
        if method(valid_urls):
            print(f"\n🎉 Success! PDF created with {len(valid_urls)} pages.")
            break
    else:
        print("\n😞 All methods failed. Please check:")
        print("1. wkhtmltopdf installation and path")
        print("2. Internet connectivity")
        print("3. Firewall/antivirus blocking wkhtmltopdf")

if __name__ == "__main__":
    main()
