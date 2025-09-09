import os
import json
from flask import Flask, render_template_string, request, jsonify
from sqlalchemy import text, create_engine
import sqlglot
import sqlparse

app = Flask(__name__)

# Set environment variable directly in the file
os.environ['DATABASE_URL'] = (
    "postgresql://neondb_owner:npg_cgKWXQH35abk@ep-summer-hall-a1ljuhxz-pooler.ap-southeast-1.aws.neon.tech/neondb"
)

# Create engine globally
engine = create_engine(os.getenv('DATABASE_URL'), echo=False)

def translate_tsql_to_postgresql(tsql_query):
    """Translate T-SQL query to PostgreSQL syntax using sqlglot with custom fixes"""
    try:
        # Parse and transpile T-SQL to PostgreSQL
        parsed = sqlglot.transpile(tsql_query, read="tsql", write="postgres")[0]
        
        # Fix common PostgreSQL compatibility issues
        # Replace GENERATED AS IDENTITY with SERIAL
        import re
        parsed = re.sub(r'\bINT\s+GENERATED\s+AS\s+IDENTITY\s*\([^)]*\)', 'SERIAL', parsed, flags=re.IGNORECASE)
        parsed = re.sub(r'\bINTEGER\s+GENERATED\s+AS\s+IDENTITY\s*\([^)]*\)', 'SERIAL', parsed, flags=re.IGNORECASE)
        
        # Fix NVARCHAR to VARCHAR
        parsed = re.sub(r'\bNVARCHAR\b', 'VARCHAR', parsed, flags=re.IGNORECASE)
        
        # Fix DATETIME2 to TIMESTAMP
        parsed = re.sub(r'\bDATETIME2\b', 'TIMESTAMP', parsed, flags=re.IGNORECASE)
        
        # Fix GETDATE() to CURRENT_TIMESTAMP
        parsed = re.sub(r'\bGETDATE\(\)', 'CURRENT_TIMESTAMP', parsed, flags=re.IGNORECASE)
        
        return {
            'success': True,
            'translated_query': parsed,
            'original_query': tsql_query
        }
    except Exception as e:
        # Fallback: apply basic regex replacements if sqlglot fails
        try:
            fallback_query = tsql_query
            import re
            
            # Basic T-SQL to PostgreSQL conversions
            fallback_query = re.sub(r'\bINT\s+IDENTITY\s*\(\s*\d+\s*,\s*\d+\s*\)', 'SERIAL', fallback_query, flags=re.IGNORECASE)
            fallback_query = re.sub(r'\bNVARCHAR\b', 'VARCHAR', fallback_query, flags=re.IGNORECASE)
            fallback_query = re.sub(r'\bDATETIME2\b', 'TIMESTAMP', fallback_query, flags=re.IGNORECASE)
            fallback_query = re.sub(r'\bGETDATE\(\)', 'CURRENT_TIMESTAMP', fallback_query, flags=re.IGNORECASE)
            fallback_query = re.sub(r'\bTOP\s+(\d+)\b', r'LIMIT \1', fallback_query, flags=re.IGNORECASE)
            
            return {
                'success': True,
                'translated_query': fallback_query,
                'original_query': tsql_query,
                'note': 'Used fallback translation due to parsing error'
            }
        except Exception as fallback_error:
            return {
                'success': False,
                'error': f"Translation error: {str(e)}. Fallback also failed: {str(fallback_error)}",
                'original_query': tsql_query,
                'translated_query': tsql_query  # Fallback to original
            }

def execute_sql(sql_query):
    """Execute SQL query and return results (with T-SQL to PostgreSQL translation)"""
    # First, translate T-SQL to PostgreSQL
    translation_result = translate_tsql_to_postgresql(sql_query)
    
    if not translation_result['success']:
        return {
            'success': False,
            'error': translation_result['error'],
            'message': translation_result['error'],
            'original_query': translation_result['original_query'],
            'translated_query': translation_result['translated_query']
        }
    
    # Use the translated query for execution
    postgres_query = translation_result['translated_query']
    
    try:
        with engine.connect() as conn:
            # Handle different types of SQL statements
            if postgres_query.strip().upper().startswith(('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN', 'WITH')):
                result = conn.execute(text(postgres_query))
                rows = result.fetchall()
                columns = list(result.keys()) if rows else []
                return {
                    'success': True,
                    'columns': columns,
                    'rows': [dict(zip(columns, row)) for row in rows],
                    'message': f'Query executed successfully. {len(rows)} rows returned.',
                    'original_query': translation_result['original_query'],
                    'translated_query': postgres_query
                }
            else:
                # For DDL/DML statements
                conn.execute(text(postgres_query))
                conn.commit()
                return {
                    'success': True,
                    'columns': [],
                    'rows': [],
                    'message': 'Command executed successfully.',
                    'original_query': translation_result['original_query'],
                    'translated_query': postgres_query
                }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': f'Execution Error: {str(e)}',
            'original_query': translation_result['original_query'],
            'translated_query': postgres_query
        }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/execute', methods=['POST'])
def execute_query():
    """Execute SQL query endpoint"""
    data = request.get_json()
    sql_query = data.get('query', '').strip()
    
    if not sql_query:
        return jsonify({'success': False, 'error': 'No query provided'})
    
    result = execute_sql(sql_query)
    return jsonify(result)

@app.route('/examples')
def get_examples():
    """Get T-SQL examples for DDL, DML, and procedures"""
    examples = {
        'ddl': [
            {
                'title': 'Create Table (T-SQL)',
                'sql': '''CREATE TABLE employees (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE,
    department NVARCHAR(50),
    salary DECIMAL(10,2),
    created_at DATETIME2 DEFAULT GETDATE()
);'''
            },
            {
                'title': 'Add Column (T-SQL)',
                'sql': 'ALTER TABLE employees ADD phone NVARCHAR(20);'
            },
            {
                'title': 'Create Index (T-SQL)',
                'sql': 'CREATE NONCLUSTERED INDEX idx_employees_department ON employees(department);'
            }
        ],
        'dml': [
            {
                'title': 'Insert Data (T-SQL)',
                'sql': '''INSERT INTO employees (name, email, department, salary) 
VALUES 
    (N'John Doe', N'john@example.com', N'Engineering', 75000),
    (N'Jane Smith', N'jane@example.com', N'Marketing', 65000);'''
            },
            {
                'title': 'Update Data (T-SQL)',
                'sql': '''UPDATE employees 
SET salary = salary * 1.1 
WHERE department = N'Engineering';'''
            },
            {
                'title': 'Select with CTE (T-SQL)',
                'sql': '''WITH HighEarners AS (
    SELECT name, department, salary,
           ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rn
    FROM employees
    WHERE salary > 60000
)
SELECT name, department, salary
FROM HighEarners
WHERE rn <= 3
ORDER BY salary DESC;'''
            }
        ],
        'procedures': [
            {
                'title': 'Stored Procedure (T-SQL)',
                'sql': '''CREATE PROCEDURE GetEmployeeCount
AS
BEGIN
    SELECT COUNT(*) AS TotalEmployees FROM employees;
END;'''
            },
            {
                'title': 'Procedure with Parameters (T-SQL)',
                'sql': '''CREATE PROCEDURE GetEmployeesByDept
    @DeptName NVARCHAR(50)
AS
BEGIN
    SELECT name, email, salary
    FROM employees
    WHERE department = @DeptName;
END;'''
            },
            {
                'title': 'Function (T-SQL)',
                'sql': '''CREATE FUNCTION dbo.CalculateBonus(@salary DECIMAL(10,2))
RETURNS DECIMAL(10,2)
AS
BEGIN
    DECLARE @bonus DECIMAL(10,2);
    SET @bonus = @salary * 0.10;
    RETURN @bonus;
END;'''
            }
        ]
    }
    return jsonify(examples)

# HTML Template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>T-SQL to PostgreSQL Editor - Neon Database</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #ffffff;
            height: 100vh;
            overflow: hidden;
        }

        .header {
            background-color: #2d2d30;
            padding: 10px 20px;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .header h1 {
            color: #ffffff;
            font-size: 18px;
        }

        .status {
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 12px;
            background-color: #0e639c;
        }

        .container {
            display: flex;
            height: calc(100vh - 60px);
        }

        .left-panel {
            width: 30%;
            background-color: #252526;
            border-right: 1px solid #3e3e42;
            display: flex;
            flex-direction: column;
        }

        .examples-header {
            padding: 15px;
            background-color: #2d2d30;
            border-bottom: 1px solid #3e3e42;
            font-weight: bold;
        }

        .examples-content {
            flex: 1;
            overflow-y: auto;
            padding: 10px;
        }

        .example-category {
            margin-bottom: 20px;
        }

        .category-title {
            color: #4fc3f7;
            font-weight: bold;
            margin-bottom: 10px;
            font-size: 14px;
            text-transform: uppercase;
        }

        .example-item {
            background-color: #2d2d30;
            border: 1px solid #3e3e42;
            border-radius: 4px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .example-item:hover {
            background-color: #094771;
        }

        .example-title {
            padding: 8px 12px;
            font-weight: 500;
            font-size: 13px;
        }

        .right-panel {
            width: 70%;
            display: flex;
            flex-direction: column;
        }

        .editor-container {
            flex: 1;
            display: flex;
            flex-direction: column;
        }

        .editor-header {
            padding: 10px 15px;
            background-color: #2d2d30;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .editor-title {
            font-weight: bold;
            color: #ffffff;
        }

        .execute-btn {
            background-color: #0e639c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            transition: background-color 0.2s;
        }

        .execute-btn:hover {
            background-color: #1177bb;
        }

        .execute-btn:disabled {
            background-color: #666;
            cursor: not-allowed;
        }

        .sql-editor {
            flex: 1;
            background-color: #1e1e1e;
            color: #d4d4d4;
            border: none;
            padding: 15px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            resize: none;
            outline: none;
        }

        .output-container {
            height: 40%;
            border-top: 1px solid #3e3e42;
            display: flex;
            flex-direction: column;
        }

        .output-header {
            padding: 10px 15px;
            background-color: #2d2d30;
            border-bottom: 1px solid #3e3e42;
            font-weight: bold;
        }

        .output-content {
            flex: 1;
            overflow: auto;
            padding: 15px;
            background-color: #1e1e1e;
        }

        .result-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        .result-table th,
        .result-table td {
            border: 1px solid #3e3e42;
            padding: 8px 12px;
            text-align: left;
        }

        .result-table th {
            background-color: #2d2d30;
            font-weight: bold;
        }

        .result-table tr:nth-child(even) {
            background-color: #252526;
        }

        .error-message {
            color: #f48771;
            background-color: #2d1b1b;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #f48771;
        }

        .success-message {
            color: #4caf50;
            background-color: #1b2d1b;
            padding: 10px;
            border-radius: 4px;
            border-left: 4px solid #4caf50;
        }

        .tutorial-section {
            background-color: #2d2d30;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }

        .tutorial-title {
            color: #4fc3f7;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .tutorial-steps {
            list-style: none;
            counter-reset: step-counter;
        }

        .tutorial-steps li {
            counter-increment: step-counter;
            margin-bottom: 8px;
            padding-left: 30px;
            position: relative;
        }

        .tutorial-steps li::before {
            content: counter(step-counter);
            position: absolute;
            left: 0;
            top: 0;
            background-color: #0e639c;
            color: white;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>T-SQL to PostgreSQL Editor - Neon Database</h1>
        <div class="status">Connected</div>
    </div>

    <div class="container">
        <div class="left-panel">
            <div class="examples-header">
                SQL Examples & Tutorial
            </div>
            <div class="examples-content">
                <div class="tutorial-section">
                    <div class="tutorial-title">Getting Started with T-SQL Translation</div>
                    <ol class="tutorial-steps">
                        <li>Write T-SQL queries using SQL Server syntax</li>
                        <li>Queries are automatically translated to PostgreSQL</li>
                        <li>Both original and translated queries are shown</li>
                        <li>Use T-SQL specific features like IDENTITY, NVARCHAR, etc.</li>
                        <li>Create stored procedures and functions using T-SQL syntax</li>
                    </ol>
                </div>

                <div id="examples-container">
                    <!-- Examples will be loaded here -->
                </div>
            </div>
        </div>

        <div class="right-panel">
            <div class="editor-container">
                <div class="editor-header">
                    <div class="editor-title">T-SQL Editor</div>
                    <button class="execute-btn" onclick="executeQuery()">Execute Query</button>
                </div>
                <textarea class="sql-editor" id="sqlEditor" placeholder="-- Write your T-SQL query here (will be auto-translated to PostgreSQL)
-- Example: SELECT TOP 10 * FROM employees;

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');"></textarea>
            </div>

            <div class="output-container">
                <div class="output-header">
                    Query Results
                </div>
                <div class="output-content" id="outputContent">
                    <div class="success-message">
                        Ready to execute SQL queries. Click an example on the left or write your own query above.
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let examples = {};

        // Load examples on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadExamples();
        });

        async function loadExamples() {
            try {
                const response = await fetch('/examples');
                examples = await response.json();
                renderExamples();
            } catch (error) {
                console.error('Error loading examples:', error);
            }
        }

        function renderExamples() {
            const container = document.getElementById('examples-container');
            
            Object.keys(examples).forEach(category => {
                const categoryDiv = document.createElement('div');
                categoryDiv.className = 'example-category';
                
                const categoryTitle = document.createElement('div');
                categoryTitle.className = 'category-title';
                categoryTitle.textContent = category.toUpperCase();
                categoryDiv.appendChild(categoryTitle);
                
                examples[category].forEach(example => {
                    const exampleDiv = document.createElement('div');
                    exampleDiv.className = 'example-item';
                    exampleDiv.onclick = () => loadExample(example.sql);
                    
                    const titleDiv = document.createElement('div');
                    titleDiv.className = 'example-title';
                    titleDiv.textContent = example.title;
                    exampleDiv.appendChild(titleDiv);
                    
                    categoryDiv.appendChild(exampleDiv);
                });
                
                container.appendChild(categoryDiv);
            });
        }

        function loadExample(sql) {
            document.getElementById('sqlEditor').value = sql;
        }

        async function executeQuery() {
            const query = document.getElementById('sqlEditor').value.trim();
            const outputContent = document.getElementById('outputContent');
            const executeBtn = document.querySelector('.execute-btn');
            
            if (!query) {
                outputContent.innerHTML = '<div class="error-message">Please enter a SQL query.</div>';
                return;
            }
            
            executeBtn.disabled = true;
            executeBtn.textContent = 'Executing...';
            outputContent.innerHTML = '<div class="success-message">Executing query...</div>';
            
            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });
                
                const result = await response.json();
                displayResult(result);
            } catch (error) {
                outputContent.innerHTML = `<div class="error-message">Network error: ${error.message}</div>`;
            } finally {
                executeBtn.disabled = false;
                executeBtn.textContent = 'Execute Query';
            }
        }

        function displayResult(result) {
            const outputContent = document.getElementById('outputContent');
            
            if (!result.success) {
                let html = `<div class="error-message">${result.message || result.error}</div>`;
                
                // Show translation info even on error
                if (result.original_query && result.translated_query) {
                    html += '<div style="margin-top: 15px;">';
                    html += '<div style="color: #4fc3f7; font-weight: bold; margin-bottom: 5px;">Original T-SQL:</div>';
                    html += `<pre style="background: #2d2d30; padding: 10px; border-radius: 4px; overflow-x: auto;">${result.original_query}</pre>`;
                    html += '<div style="color: #4fc3f7; font-weight: bold; margin: 10px 0 5px 0;">Translated PostgreSQL:</div>';
                    html += `<pre style="background: #2d2d30; padding: 10px; border-radius: 4px; overflow-x: auto;">${result.translated_query}</pre>`;
                    html += '</div>';
                }
                
                outputContent.innerHTML = html;
                return;
            }
            
            let html = `<div class="success-message">${result.message}</div>`;
            
            // Show translation info
            if (result.original_query && result.translated_query) {
                html += '<div style="margin-top: 15px;">';
                html += '<div style="color: #4fc3f7; font-weight: bold; margin-bottom: 5px;">Original T-SQL:</div>';
                html += `<pre style="background: #2d2d30; padding: 10px; border-radius: 4px; overflow-x: auto; color: #d4d4d4; font-family: Consolas, Monaco, monospace; font-size: 13px;">${result.original_query}</pre>`;
                html += '<div style="color: #4fc3f7; font-weight: bold; margin: 10px 0 5px 0;">Translated PostgreSQL:</div>';
                html += `<pre style="background: #2d2d30; padding: 10px; border-radius: 4px; overflow-x: auto; color: #d4d4d4; font-family: Consolas, Monaco, monospace; font-size: 13px;">${result.translated_query}</pre>`;
                html += '</div>';
            }
            
            if (result.rows && result.rows.length > 0) {
                html += '<div style="color: #4fc3f7; font-weight: bold; margin: 15px 0 5px 0;">Query Results:</div>';
                html += '<table class="result-table">';
                
                // Headers
                html += '<thead><tr>';
                result.columns.forEach(col => {
                    html += `<th>${col}</th>`;
                });
                html += '</tr></thead>';
                
                // Rows
                html += '<tbody>';
                result.rows.forEach(row => {
                    html += '<tr>';
                    result.columns.forEach(col => {
                        const value = row[col];
                        html += `<td>${value !== null ? value : 'NULL'}</td>`;
                    });
                    html += '</tr>';
                });
                html += '</tbody></table>';
            }
            
            outputContent.innerHTML = html;
        }

        // Allow Ctrl+Enter to execute query
        document.getElementById('sqlEditor').addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                executeQuery();
            }
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


# pip install Flask==2.3.3 SQLAlchemy==2.0.21 psycopg2-binary==2.9.7