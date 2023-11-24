from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store arguments temporarily
debate_arguments = defaultdict(dict)


@app.route('/debate/<room_id>')
def debate_room(room_id):
    return render_template('debate_room.html', room_id=room_id)


@socketio.on('submit_argument')
def handle_argument_submission(data):
    room = data['room']
    username = data['username']  # You'll need to manage usernames
    argument = data['argument']

    debate_arguments[room][username] = argument

    if len(debate_arguments[room]) == 2:  # Check if both arguments are submitted
        # Emit the arguments to both players
        emit('arguments_submitted', debate_arguments[room], room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
