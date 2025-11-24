# Photo Guessing Game

A simple web application for organizing weekly photo guessing games with your team.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python3 app.py
```

3. Access the app:
- Locally: `http://localhost:5001`
- On your network: `http://YOUR_IP_ADDRESS:5001`

To find your IP address on Mac:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## How to Use

### Phase 1: Collection
1. Share the URL with your team
2. Each person uploads a photo and enters their name
3. When ready, click "Start Voting"

### Phase 2: Voting
1. Everyone visits `/voting`
2. Each person enters their name and guesses who owns each photo
3. Submit votes

### Phase 3: Results
1. Visit `/results` to see:
   - Winner (person with most correct guesses)
   - Leaderboard
   - Photo reveal (who actually owns each photo)

## File Structure

- `app.py` - Main Flask application
- `templates/` - HTML templates
- `static/` - CSS and uploaded photos
- `data/game_data.json` - Game state storage

## Resetting the Game

To reset for a new week, delete `data/game_data.json` and restart the app.

