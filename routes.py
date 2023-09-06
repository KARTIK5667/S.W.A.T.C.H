from flask import render_template, request, url_for, redirect, session, jsonify
from controllers import register_patient, edit_patient, register_user, login_user, logout_user, get_data, update_data, dashboard
from __main__ import app

# Register routes
app.add_url_rule('/editpatient', 'edit_patients', edit_patient, methods=['POST', 'GET'])
app.add_url_rule('/addpatient', 'add_patients', register_patient, methods=['POST', 'GET'])
app.add_url_rule('/', 'index', register_user, methods=['POST', 'GET'])
app.add_url_rule('/login', 'login', login_user, methods=['POST', 'GET'])
app.add_url_rule('/logged_in', 'logged_in', dashboard)
app.add_url_rule('/logout', 'logout', logout_user, methods=['POST', 'GET'])
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/data', 'get_data', get_data, methods=['GET'])
app.add_url_rule('/update_data', 'update_data', update_data, methods=['POST'])
