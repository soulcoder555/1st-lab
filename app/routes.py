from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

main = Blueprint('main', __name__)

challenges = [
    {
        'id': 1,
        'title': 'SQL Injection - Login Bypass',
        'vulnerability_type': 'SQL Injection',
        'difficulty': 'Beginner',
        'points': 150,
        'description': 'Bypass authentication using SQL injection against a login form.',
        'exploitation_steps': [
            {'step': 1, 'title': 'Inspect the form', 'description': 'Identify the username and password fields.'},
            {'step': 2, 'title': 'Inject payload', 'description': "Submit payload such as ' OR '1'='1 to bypass authentication."},
            {'step': 3, 'title': 'Verify access', 'description': 'Confirm you are logged in without valid credentials.'}
        ],
        'attack_payloads': [
            {'name': 'Login bypass', 'payload': "' OR '1'='1", 'explanation': 'Always-true SQL condition.', 'expected_result': 'Authentication bypassed.'}
        ],
        'security_defenses': [
            {'defense_name': 'Parameterized queries', 'how_it_works': 'Separates SQL code from user input.', 'bypass_method': 'Not bypassable when implemented correctly.'}
        ],
        'cvss_score': 8.8,
        'cwe_id': 'CWE-89',
        'lab_environment': 'SQL Injection Lab'
    },
    {
        'id': 2,
        'title': 'Stored XSS - Comment Board',
        'vulnerability_type': 'Stored XSS',
        'difficulty': 'Intermediate',
        'points': 220,
        'description': 'Store a malicious script in comments that executes for other users.',
        'exploitation_steps': [
            {'step': 1, 'title': 'Locate the comment field', 'description': 'Find a persistent form that displays user comments.'},
            {'step': 2, 'title': 'Submit script payload', 'description': 'Use <script>alert(1)</script> or similar.'},
            {'step': 3, 'title': 'View as another user', 'description': 'Confirm the payload executes when the comment is viewed.'}
        ],
        'attack_payloads': [
            {'name': 'Stored XSS', 'payload': '<script>alert("xss")</script>', 'explanation': 'Stores script on server and executes in browser.', 'expected_result': 'Alert or script executes.'}
        ],
        'security_defenses': [
            {'defense_name': 'Output encoding', 'how_it_works': 'Escapes HTML before rendering.', 'bypass_method': 'Prevents raw script execution.'}
        ],
        'cvss_score': 9.0,
        'cwe_id': 'CWE-79',
        'lab_environment': 'Stored XSS Lab'
    }
]

vulnerabilities = [
    {
        'id': 1,
        'name': 'SQL Injection',
        'severity': 'Critical',
        'category': 'Injection',
        'description': 'Injection of SQL commands through untrusted input.',
        'testing_methodology': 'Review form inputs, try quote-terminated payloads, and analyze responses.',
        'real_world_impact': 'Can lead to data theft, authentication bypass, and full database compromise.',
        'mitigation_checklist': [
            {'item': 'Use parameterized queries', 'priority': 'High', 'implementation': 'Use prepared statements with bound parameters.'},
            {'item': 'Validate input types', 'priority': 'High', 'implementation': 'Reject incorrect input formats before querying.'}
        ],
        'tool_recommendations': [
            {'tool_name': 'sqlmap', 'command': "sqlmap -u 'http://localhost:6000/login' --data='username=admin&password=PASS'", 'output_interpretation': 'Look for injection points and database names.'}
        ],
        'cwe_id': 'CWE-89',
        'owasp_category': 'A03:2021 - Injection'
    },
    {
        'id': 2,
        'name': 'Stored Cross-Site Scripting (XSS)',
        'severity': 'Critical',
        'category': 'Client-side Attacks',
        'description': 'User-supplied scripts are stored and then executed in other users’ browsers.',
        'testing_methodology': 'Submit payloads, reload pages, and observe execution in browser context.',
        'real_world_impact': 'Can steal sessions, perform actions on behalf of users, or inject malicious content.',
        'mitigation_checklist': [
            {'item': 'Encode output', 'priority': 'High', 'implementation': 'HTML-encode all user-controlled content.'},
            {'item': 'Use CSP', 'priority': 'Medium', 'implementation': 'Add a strict Content Security Policy.'}
        ],
        'tool_recommendations': [
            {'tool_name': 'Burp Suite', 'command': 'Use Repeater to inject and inspect payloads.', 'output_interpretation': 'Confirm the payload is stored and rendered without escaping.'}
        ],
        'cwe_id': 'CWE-79',
        'owasp_category': 'A07:2021 - Identification and Authentication Failures'
    }
]

labs = [
    {
        'id': 1,
        'name': 'SQL Injection Lab',
        'environment_type': 'vulnerable_flask',
        'description': 'A vulnerable login page designed to teach SQL injection fundamentals.',
        'intentional_vulnerabilities': [
            {'vuln_name': 'SQL Injection', 'location': 'login endpoint', 'how_to_exploit': "Submit ' OR '1'='1", 'expected_result': 'Bypass login'}
        ],
        'status': 'stopped',
        'provisioned_at': None,
        'reset_script': 'RESET SQLI LAB STATE'
    },
    {
        'id': 2,
        'name': 'Stored XSS Lab',
        'environment_type': 'vulnerable_flask',
        'description': 'A simple comment board that stores injected scripts.',
        'intentional_vulnerabilities': [
            {'vuln_name': 'Stored XSS', 'location': 'comment submission', 'how_to_exploit': '<script>alert(1)</script>', 'expected_result': 'Script executes in browser'}
        ],
        'status': 'stopped',
        'provisioned_at': None,
        'reset_script': 'RESET XSS LAB STATE'
    }
]

user_activity = []

@main.route('/')
def home():
    return render_template('home.html', challenges=challenges, vulnerabilities=vulnerabilities, labs=labs, activity=user_activity)

@main.route('/challenges')
def challenge_list():
    return render_template('challenges.html', challenges=challenges)

@main.route('/challenge/<int:challenge_id>')
def challenge_detail(challenge_id):
    challenge = next((item for item in challenges if item['id'] == challenge_id), None)
    if not challenge:
        return 'Challenge not found', 404
    return render_template('challenge_detail.html', challenge=challenge)

@main.route('/submit/<int:challenge_id>', methods=['POST'])
def submit_challenge(challenge_id):
    proof = request.form.get('proof', '').strip()
    if not proof:
        flash('Proof is required to submit.', 'error')
        return redirect(url_for('main.challenge_detail', challenge_id=challenge_id))
    user_activity.append({'challenge_id': challenge_id, 'proof': proof, 'timestamp': datetime.utcnow().isoformat(), 'success': True})
    flash('Proof submitted successfully.', 'success')
    return redirect(url_for('main.challenge_detail', challenge_id=challenge_id))

@main.route('/vulnerabilities')
def vulnerability_list():
    return render_template('vulnerabilities.html', vulnerabilities=vulnerabilities)

@main.route('/vulnerability/<int:vuln_id>')
def vulnerability_detail(vuln_id):
    vuln = next((item for item in vulnerabilities if item['id'] == vuln_id), None)
    if not vuln:
        return 'Vulnerability not found', 404
    return render_template('vulnerability_detail.html', vulnerability=vuln)

@main.route('/labs')
def lab_list():
    return render_template('labs.html', labs=labs)

@main.route('/lab/<int:lab_id>')
def lab_detail(lab_id):
    lab = next((item for item in labs if item['id'] == lab_id), None)
    if not lab:
        return 'Lab not found', 404
    return render_template('lab_detail.html', lab=lab)

@main.route('/lab/<int:lab_id>/provision', methods=['POST'])
def lab_provision(lab_id):
    lab = next((item for item in labs if item['id'] == lab_id), None)
    if not lab:
        return 'Lab not found', 404
    lab['status'] = 'running'
    lab['provisioned_at'] = datetime.utcnow().isoformat()
    flash(f'{lab["name"]} provisioned successfully.', 'success')
    return redirect(url_for('main.lab_detail', lab_id=lab_id))
