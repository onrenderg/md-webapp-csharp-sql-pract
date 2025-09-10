from flask import Flask, render_template, request, jsonify, redirect, url_for
import markdown
import os
import re
import sqlparse
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json
from datetime import datetime, date
import decimal

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
RESOURCES_DIR = os.path.join(app.root_path, 'resources')
app.config['RESOURCES_DIR'] = RESOURCES_DIR
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

# Custom JSON encoder for database results
class DatabaseJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return super().default(obj)

def get_db_connection():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(app.config['DATABASE_URL'])
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch_results=True):
    """Execute a query safely with proper error handling"""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if not conn:
            return {'success': False, 'error': 'Database connection failed'}
        
        # Use RealDictCursor for better result formatting
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Execute query with parameters (safe from SQL injection)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Handle different query types
        query_type = query.strip().upper().split()[0] if query.strip() else ''
        
        if query_type in ['SELECT', 'SHOW', 'DESCRIBE', 'WITH']:
            if fetch_results:
                results = cursor.fetchall()
                return {
                    'success': True,
                    'rows': results,
                    'rowcount': len(results),
                    'columns': [desc[0] for desc in cursor.description] if cursor.description else []
                }
        elif query_type in ['INSERT', 'UPDATE', 'DELETE']:
            conn.commit()
            return {
                'success': True,
                'rowcount': cursor.rowcount,
                'message': f'{query_type} executed successfully. {cursor.rowcount} row(s) affected.'
            }
        elif query_type in ['CREATE', 'ALTER', 'DROP']:
            conn.commit()
            return {
                'success': True,
                'message': f'{query_type} statement executed successfully.'
            }
        else:
            conn.commit()
            return {
                'success': True,
                'message': 'Query executed successfully.'
            }
            
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        return {
            'success': False,
            'error': f"Database error: {str(e)}",
            'error_code': e.pgcode if hasattr(e, 'pgcode') else None
        }
    except Exception as e:
        if conn:
            conn.rollback()
        return {
            'success': False,
            'error': f"Unexpected error: {str(e)}"
        }
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_markdown_files():
    """Get all markdown files from the resources directory"""
    markdown_files = []
    if os.path.exists(RESOURCES_DIR):
        for filename in os.listdir(RESOURCES_DIR):
            if filename.endswith('.md'):
                name = filename[:-3]  # Remove .md extension
                markdown_files.append({
                    'name': name,
                    'filename': filename,
                    'title': name.replace('-', ' ').title()
                })
    return sorted(markdown_files, key=lambda x: x['name'])

def process_markdown_links(content, current_file=None):
    """Process [label](./path) links to convert them to Flask routes"""
    def replace_link(match):
        label = match.group(1)
        path = match.group(2)
        if path.startswith('./'):
            # Remove ./ and add .md if not present
            page_name = path[2:]
            if not page_name.endswith('.md'):
                page_name += '.md'
            # Convert to route
            route_name = page_name[:-3]  # Remove .md
            return f'[{label}](/page/{route_name})'
        return match.group(0)
    
    # Match [label](./path) pattern
    pattern = r'\[([^\]]+)\]\(\.\/([^)]+)\)'
    return re.sub(pattern, replace_link, content)

def render_markdown(filepath):
    """Render markdown file to HTML"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process custom links
        content = process_markdown_links(content)
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['codehilite', 'fenced_code'])
        html_content = md.convert(content)
        
        return html_content
    except Exception as e:
        return f"<p>Error rendering markdown: {str(e)}</p>"

@app.route('/')
def index():
    """Home page - redirect to first available markdown file or show welcome"""
    markdown_files = get_markdown_files()
    if markdown_files:
        return redirect(url_for('show_page', page_name=markdown_files[0]['name']))
    return render_template('index.html', 
                         markdown_files=markdown_files, 
                         content="<h1>Welcome</h1><p>No markdown files found in resources directory.</p>")

@app.route('/page/<page_name>')
def show_page(page_name):
    """Show specific markdown page"""
    markdown_files = get_markdown_files()
    
    # Find the requested file
    filepath = os.path.join(RESOURCES_DIR, f"{page_name}.md")
    
    if os.path.exists(filepath):
        content = render_markdown(filepath)
        current_page = page_name
    else:
        content = f"<h1>Page Not Found</h1><p>The page '{page_name}' was not found.</p>"
        current_page = None
    
    return render_template('index.html', 
                         markdown_files=markdown_files, 
                         content=content,
                         current_page=current_page)

@app.route('/api/execute_sql', methods=['POST'])
def execute_sql():
    """Execute SQL code against PostgreSQL database"""
    try:
        sql_code = request.json.get('sql', '')
        demo_mode = request.json.get('demo_mode', False)
        
        # Parse and format SQL
        formatted_sql = sqlparse.format(sql_code, reindent=True, keyword_case='upper')
        
        # If no database URL is configured or demo mode is requested, just format
        if not app.config['DATABASE_URL'] or demo_mode:
            # Syntax highlighting
            lexer = SqlLexer()
            formatter = HtmlFormatter(style='default', noclasses=True)
            highlighted = highlight(formatted_sql, lexer, formatter)
            
            return jsonify({
                'success': True,
                'result': 'SQL formatted successfully (Demo Mode)',
                'formatted_sql': highlighted,
                'message': 'Note: Running in demo mode. Configure DATABASE_URL to execute queries.',
                'demo_mode': True
            })
        
        # Execute the query against the database
        result = execute_query(sql_code)
        
        if result['success']:
            response = {
                'success': True,
                'formatted_sql': formatted_sql
            }
            
            # Add appropriate response based on query result
            if 'rows' in result:
                # Convert rows to JSON-serializable format
                response['rows'] = json.loads(
                    json.dumps(result['rows'], cls=DatabaseJSONEncoder)
                )
                response['columns'] = result.get('columns', [])
                response['rowcount'] = result.get('rowcount', 0)
                response['message'] = f"Query executed successfully. {result['rowcount']} row(s) returned."
            elif 'message' in result:
                response['message'] = result['message']
                if 'rowcount' in result:
                    response['rowcount'] = result['rowcount']
            
            return jsonify(response)
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error occurred'),
                'error_code': result.get('error_code')
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        })

if __name__ == '__main__':
    # Create resources directory if it doesn't exist
    os.makedirs(RESOURCES_DIR, exist_ok=True)
    app.run(debug=True, port=5000)
