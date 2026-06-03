from flask import Flask, render_template, request, jsonify
from board import Board
from ai import ConnectFourAI
from constants import *

app = Flask(__name__)

# Game instances initialized globally in-memory
board_state = Board()
ai_engine = ConnectFourAI(HARD)

@app.route('/')
def index():
    global board_state
    board_state = Board()  # Reset upon landing/page refreshes
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board_state, ai_engine
    data = request.get_json()
    
    col = int(data.get('column'))
    difficulty = data.get('difficulty', HARD)
    ai_engine.difficulty = difficulty

    # 1. Process Human action
    if not board_state.is_valid_location(col):
        return jsonify({'error': 'Column full!'}), 400
        
    row = board_state.get_next_open_row(col)
    board_state.drop_piece(row, col, PLAYER)

    if board_state.check_win(PLAYER):
        return jsonify({'board': board_state.grid.tolist(), 'status': 'win', 'winner': 'Human'})
    if board_state.is_draw():
        return jsonify({'board': board_state.grid.tolist(), 'status': 'draw'})

    # 2. Compute AI action response
    ai_col = ai_engine.choose_move(board_state)
    if ai_col is not None:
        ai_row = board_state.get_next_open_row(ai_col)
        board_state.drop_piece(ai_row, ai_col, AI)

        if board_state.check_win(AI):
            return jsonify({'board': board_state.grid.tolist(), 'status': 'win', 'winner': 'AI'})
        if board_state.is_draw():
            return jsonify({'board': board_state.grid.tolist(), 'status': 'draw'})

    return jsonify({'board': board_state.grid.tolist(), 'status': 'ongoing'})

@app.route('/reset', methods=['POST'])
def reset():
    global board_state
    board_state = Board()
    return jsonify({'status': 'reset', 'board': board_state.grid.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
