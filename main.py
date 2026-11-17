import chess

def evaluate_board(board: chess.Board) -> int:
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    piece_values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            val = piece_values.get(piece.piece_type, 0)
            if piece.color == board.turn:
                score += val
            else:
                score -= val
    return score

def minimax(board: chess.Board, depth: int, maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if maximizing:
        max_eval = -999999
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = 999999
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def get_move(board: chess.Board) -> chess.Move:
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None

    best_move = legal_moves[0]
    best_value = -999999
    
    for move in legal_moves:
        board.push(move)
        value = -minimax(board, 1, False)
        board.pop()
        
        if value > best_value:
            best_value = value
            best_move = move

    return best_move
