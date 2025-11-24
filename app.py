from flask import Flask, render_template, request, jsonify, send_from_directory, session
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
# Master password - always works (change this to something secure!)
MASTER_PASSWORD = os.environ.get('MASTER_PASSWORD', 'master-admin-2024')
# Weekly host password - set via environment variable, changes each week
HOST_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # Use environment variable, default for local dev

DATA_FILE = 'data/game_data.json'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('data', exist_ok=True)

def init_game_data():
    """Initialize game data file if it doesn't exist"""
    if not os.path.exists(DATA_FILE):
        data = {
            'photos': [],
            'voters': [],
            'votes': {},
            'phase': 'collection',
            'voting_enabled': False,
            'revealed_photos': [],  # List of photo IDs that have been revealed
            'created_at': datetime.now().isoformat()
        }
        save_game_data(data)
    return load_game_data()

def load_game_data():
    """Load game data from JSON file"""
    if not os.path.exists(DATA_FILE):
        return init_game_data()
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_game_data(data):
    """Save game data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def index():
    data = load_game_data()
    return render_template('index.html', 
                         photo_count=len(data['photos']),
                         phase=data['phase'],
                         photos=data['photos'],
                         voting_enabled=data.get('voting_enabled', False))

@app.route('/upload', methods=['POST'])
def upload_photo():
    data = load_game_data()
    
    if data['phase'] != 'collection':
        return jsonify({'error': 'Collection phase has ended'}), 400
    
    if 'photo' not in request.files:
        return jsonify({'error': 'No picture file provided'}), 400
    
    file = request.files['photo']
    submitter_name = request.form.get('name', '').strip()
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not submitter_name:
        return jsonify({'error': 'Please enter your name'}), 400
    
    # Check for duplicate names
    existing_names = [p['submitter'] for p in data['photos']]
    if submitter_name in existing_names:
        return jsonify({'error': f'A picture from {submitter_name} already exists'}), 400
    
    # Save file
    filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Save photo metadata
    photo_data = {
        'id': str(uuid.uuid4()),
        'filename': filename,
        'submitter': submitter_name,
        'uploaded_at': datetime.now().isoformat()
    }
    data['photos'].append(photo_data)
    save_game_data(data)
    
    return jsonify({
        'success': True,
        'message': f'Picture from {submitter_name} uploaded successfully!',
        'photo_count': len(data['photos'])
    })

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Game Host page - single page for all game host functions (password protected)"""
    # Handle login
    if request.method == 'POST':
        password = request.form.get('password', '')
        # Check both master password (always works) and weekly host password
        if password == MASTER_PASSWORD or password == HOST_PASSWORD:
            session['admin_authenticated'] = True
            return jsonify({'success': True, 'redirect': '/admin'})
        else:
            return jsonify({'success': False, 'error': 'Incorrect password'}), 401
    
    # Check authentication
    if not session.get('admin_authenticated', False):
        return render_template('admin_login.html')
    
    data = load_game_data()
    
    # Calculate voting results if there are votes
    results_summary = None
    if data.get('votes') and len(data['votes']) > 0:
        results_summary = calculate_results(data)
    
    # Build detailed results per photo for display
    photos_with_guesses = []
    if data.get('votes') and len(data['votes']) > 0:
        for photo in data['photos']:
            correct_guessers = []
            incorrect_guessers = []
            
            for voter_name, votes in data['votes'].items():
                guessed_submitter = votes.get(photo['id'], '')
                if guessed_submitter == photo['submitter']:
                    correct_guessers.append(voter_name)
                else:
                    incorrect_guessers.append({
                        'name': voter_name,
                        'guessed': guessed_submitter
                    })
            
            photos_with_guesses.append({
                'photo': photo,
                'correct_guessers': correct_guessers,
                'incorrect_guessers': incorrect_guessers
            })
    
    return render_template('admin.html', 
                         photos=data['photos'],
                         phase=data['phase'],
                         voting_enabled=data.get('voting_enabled', False),
                         photo_count=len(data['photos']),
                         voters=data.get('voters', []),
                         results=results_summary,
                         revealed_photos=data.get('revealed_photos', []),
                         photos_with_guesses=photos_with_guesses,
                         votes_data=data.get('votes', {}))

@app.route('/start_voting', methods=['POST'])
def start_voting():
    data = load_game_data()
    
    if len(data['photos']) < 2:
        return jsonify({'error': 'Need at least 2 pictures to start voting'}), 400
    
    data['phase'] = 'voting'
    data['voting_enabled'] = True
    save_game_data(data)
    
    return jsonify({'success': True, 'message': 'Voting phase started'})

@app.route('/enable_voting', methods=['POST'])
def enable_voting():
    """Enable voting (game host only)"""
    # Check authentication
    if not session.get('admin_authenticated', False):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_game_data()
    
    if len(data['photos']) < 2:
        return jsonify({'error': 'Need at least 2 pictures to enable voting'}), 400
    
    data['voting_enabled'] = True
    data['phase'] = 'voting'
    save_game_data(data)
    
    return jsonify({'success': True, 'message': 'Voting enabled'})

@app.route('/disable_voting', methods=['POST'])
def disable_voting():
    """Disable voting (game host only)"""
    # Check authentication
    if not session.get('admin_authenticated', False):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_game_data()
    data['voting_enabled'] = False
    save_game_data(data)
    
    return jsonify({'success': True, 'message': 'Voting disabled'})

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    """Logout from game host panel"""
    session.pop('admin_authenticated', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/restart_game', methods=['POST'])
def restart_game():
    """Restart the game - clears everything (game host only)"""
    # Check authentication
    if not session.get('admin_authenticated', False):
        return jsonify({'error': 'Unauthorized'}), 401
    
    """Restart the game - clears everything (game host only)"""
    data = load_game_data()
    
    # Delete all uploaded pictures
    for photo in data.get('photos', []):
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo['filename'])
        try:
            if os.path.exists(photo_path):
                os.remove(photo_path)
        except Exception as e:
            print(f"Error deleting photo {photo['filename']}: {e}")
    
    # Reset game data
    new_data = {
        'photos': [],
        'voters': [],
        'votes': {},
        'phase': 'collection',
        'voting_enabled': False,
        'created_at': datetime.now().isoformat()
    }
    save_game_data(new_data)
    
    return jsonify({'success': True, 'message': 'Game restarted successfully'})

@app.route('/voting')
def voting():
    data = load_game_data()
    
    # Check if voting is enabled
    if not data.get('voting_enabled', False):
        return render_template('index.html', 
                             photo_count=len(data['photos']),
                             phase=data['phase'],
                             photos=data['photos'],
                             voting_enabled=False)
    
    # Shuffle photos to hide order
    import random
    photos = data['photos'].copy()
    random.shuffle(photos)
    
    return render_template('voting.html', photos=photos)

@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = load_game_data()
    
    if not data.get('voting_enabled', False):
        return jsonify({'error': 'Voting is not enabled yet'}), 400
    
    voter_name = request.json.get('voter_name', '').strip()
    votes = request.json.get('votes', {})
    
    if not voter_name:
        return jsonify({'error': 'Please enter your name'}), 400
    
    if voter_name in data['voters']:
        return jsonify({'error': f'{voter_name} has already voted'}), 400
    
    if len(votes) != len(data['photos']):
        return jsonify({'error': 'Must vote for all pictures'}), 400
    
    # Save votes
    data['voters'].append(voter_name)
    data['votes'][voter_name] = votes
    save_game_data(data)
    
    return jsonify({
        'success': True,
        'message': f'Votes from {voter_name} submitted successfully',
        'voters_count': len(data['voters']),
        'redirect': '/user/results'  # Redirect to user results page
    })

@app.route('/results')
def results():
    data = load_game_data()
    
    if data['phase'] != 'voting' and data['phase'] != 'results':
        return render_template('index.html', 
                             photo_count=len(data['photos']),
                             phase=data['phase'])
    
    # Calculate results
    results_data = calculate_results(data)
    
    # Change phase to results if still in voting
    if data['phase'] == 'voting':
        data['phase'] = 'results'
        save_game_data(data)
    
    return render_template('results.html', 
                         photos=data['photos'],
                         results=results_data)

@app.route('/reveal_photo', methods=['POST'])
def reveal_photo():
    """Reveal a picture (game host only)"""
    # Check authentication
    if not session.get('admin_authenticated', False):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_game_data()
    photo_id = request.json.get('photo_id')
    
    if not photo_id:
        return jsonify({'error': 'Picture ID required'}), 400
    
    # Verify picture exists
    photo_ids = [p['id'] for p in data['photos']]
    if photo_id not in photo_ids:
        return jsonify({'error': 'Picture not found'}), 404
    
    # Add to revealed list if not already there
    if 'revealed_photos' not in data:
        data['revealed_photos'] = []
    if photo_id not in data['revealed_photos']:
        data['revealed_photos'].append(photo_id)
        save_game_data(data)
        return jsonify({'success': True, 'message': 'Picture revealed'})
    else:
        return jsonify({'success': False, 'error': 'Picture already revealed'}), 400

@app.route('/unreveal_photo', methods=['POST'])
def unreveal_photo():
    """Un-reveal a picture (game host only)"""
    # Check authentication
    if not session.get('admin_authenticated', False):
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = load_game_data()
    photo_id = request.json.get('photo_id')
    
    if not photo_id:
        return jsonify({'error': 'Picture ID required'}), 400
    
    # Verify picture exists
    photo_ids = [p['id'] for p in data['photos']]
    if photo_id not in photo_ids:
        return jsonify({'error': 'Picture not found'}), 404
    
    # Remove from revealed list if present
    if 'revealed_photos' in data and photo_id in data['revealed_photos']:
        data['revealed_photos'].remove(photo_id)
        save_game_data(data)
        return jsonify({'success': True, 'message': 'Picture un-revealed'})
    else:
        return jsonify({'success': False, 'error': 'Picture not revealed'}), 400

@app.route('/user/results')
def user_results():
    """Player-facing results page with all pictures shown, guesses revealed one by one"""
    data = load_game_data()
    
    voting_enabled = data.get('voting_enabled', False)
    revealed_ids = data.get('revealed_photos', [])
    has_votes = data.get('votes') and len(data['votes']) > 0
    has_photos = len(data['photos']) > 0
    
    # Show results page if:
    # 1. Voting is enabled, OR
    # 2. There are already votes (even if voting was disabled), OR
    # 3. There are revealed pictures (even if voting was disabled)
    # Otherwise, show waiting message
    if not voting_enabled and not has_votes and len(revealed_ids) == 0:
        return render_template('user_results.html', 
                             photos_with_guesses=[],
                             no_votes=True,
                             waiting_for_voting=True,
                             voters=[],
                             votes_data={},
                             revealed_photos=[],
                             total_photos=len(data['photos']))
    
    # Build results for all photos - show pictures, but only reveal guess info if revealed
    photos_with_guesses = []
    for photo in data['photos']:
        is_revealed = photo['id'] in revealed_ids
        
        correct_guessers = []
        incorrect_guessers = []
        
        # Only calculate guess info if this photo has been revealed
        if is_revealed and data.get('votes'):
            for voter_name, votes in data['votes'].items():
                guessed_submitter = votes.get(photo['id'], '')
                if guessed_submitter == photo['submitter']:
                    correct_guessers.append(voter_name)
                else:
                    incorrect_guessers.append({
                        'name': voter_name,
                        'guessed': guessed_submitter
                    })
        
        photos_with_guesses.append({
            'photo': photo,
            'correct_guessers': correct_guessers,
            'incorrect_guessers': incorrect_guessers,
            'is_revealed': is_revealed
        })
    
    return render_template('user_results.html', 
                         photos_with_guesses=photos_with_guesses,
                         no_votes=False,
                         total_photos=len(data['photos']),
                         revealed_count=len(revealed_ids),
                         voters=data.get('voters', []),
                         votes_data=data.get('votes', {}),
                         revealed_photos=revealed_ids)

@app.route('/admin/results')
def admin_results():
    """Game Host results page with detailed voting breakdown per picture"""
    data = load_game_data()
    
    if not data.get('votes') or len(data['votes']) == 0:
        return render_template('admin_results.html', 
                             photos=data['photos'],
                             votes={},
                             no_votes=True)
    
    # Build detailed results per picture
    photos_with_guesses = []
    for photo in data['photos']:
        correct_guessers = []
        incorrect_guessers = []
        
        for voter_name, votes in data['votes'].items():
            guessed_submitter = votes.get(photo['id'], '')
            if guessed_submitter == photo['submitter']:
                correct_guessers.append(voter_name)
            else:
                incorrect_guessers.append({
                    'name': voter_name,
                    'guessed': guessed_submitter
                })
        
        photos_with_guesses.append({
            'photo': photo,
            'correct_guessers': correct_guessers,
            'incorrect_guessers': incorrect_guessers
        })
    
    return render_template('admin_results.html', 
                         photos_with_guesses=photos_with_guesses,
                         no_votes=False)

def calculate_results(data):
    """Calculate who guessed the most correctly"""
    photos = {p['id']: p for p in data['photos']}
    scores = {}
    
    for voter_name, votes in data['votes'].items():
        correct = 0
        for photo_id, guessed_submitter in votes.items():
            actual_submitter = photos[photo_id]['submitter']
            if guessed_submitter == actual_submitter:
                correct += 1
        scores[voter_name] = {
            'correct': correct,
            'total': len(photos),
            'percentage': round((correct / len(photos)) * 100, 1) if photos else 0
        }
    
    # Sort by correct guesses
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]['correct'], reverse=True)
    
    return {
        'scores': dict(sorted_scores),
        'winner': sorted_scores[0][0] if sorted_scores else None,
        'photos_info': photos
    }

@app.route('/api/status')
def api_status():
    """API endpoint to check game status"""
    data = load_game_data()
    return jsonify({
        'voting_enabled': data.get('voting_enabled', False),
        'phase': data['phase'],
        'photo_count': len(data['photos']),
        'voters_count': len(data.get('voters', []))
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_game_data()
    # Use PORT environment variable for Render, default to 5001 for local
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

