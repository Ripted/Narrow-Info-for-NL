#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

def fetch_level_details(level_id):
    url = f"https://api.narrowarrow.xyz/level-details/{level_id}?isCustomLevel=true"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def fetch_leaderboard(level_id):
    url = f"https://api.narrowarrow.xyz/leaderboard?levelId={level_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def fetch_run_details(run_id):
    url = f"https://api.narrowarrow.xyz/runs/{run_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def format_time(seconds):
    if seconds is None:
        return "N/A"
    return f"{seconds:.3f}s"

def normalize_run_data(run):
    return {
        'run_id': run.get('runId') or run.get('run_id'),
        'completion_time': run.get('completion_time'),
        'username': run.get('username'),
        'arrow_name': run.get('arrow_name')
    }

def convert_leaderboard_to_list(leaderboard_data):
    runs = []
    if isinstance(leaderboard_data, list):
        runs = [normalize_run_data(run) for run in leaderboard_data]
    elif isinstance(leaderboard_data, dict):
        for key in sorted(leaderboard_data.keys(), key=lambda x: int(x) if str(x).isdigit() else float('inf')):
            if str(key).isdigit():
                runs.append(normalize_run_data(leaderboard_data[key]))
    return runs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/leaderboard/<level_id>')
def view_leaderboard(level_id):
    # Fetch level details and leaderboard
    level_details = fetch_level_details(level_id)
    leaderboard_data = fetch_leaderboard(level_id)
    
    if not leaderboard_data:
        return render_template('error.html', error="Failed to fetch leaderboard data")
    
    runs = convert_leaderboard_to_list(leaderboard_data)
    
    # Prepare level info
    level_info = {}
    if level_details:
        level_info_raw = level_details.get('levelInfo', {})
        level_info = {
            'name': level_info_raw.get('name', 'Unknown'),
            'author': level_info_raw.get('author', 'Unknown'),
            'created_at': level_info_raw.get('created_at', 'N/A'),
            'likes': level_info_raw.get('like_count', 0)
        }
        if isinstance(level_info['created_at'], str) and 'T' in level_info['created_at']:
            level_info['created_at'] = level_info['created_at'].split('T')[0]
    
    return render_template('leaderboard.html', 
                         level_id=level_id,
                         level_info=level_info,
                         runs=runs,
                         format_time=format_time)

@app.route('/api/run-details/<run_id>')
def api_run_details(run_id):
    details = fetch_run_details(run_id)
    if details:
        finished_at = details.get('finishedAt', 'N/A')
        if isinstance(finished_at, str) and 'T' in finished_at:
            finished_at = finished_at.split('.')[0].replace('T', ' ')
        return jsonify({'finishedAt': finished_at})
    return jsonify({'finishedAt': 'N/A'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
