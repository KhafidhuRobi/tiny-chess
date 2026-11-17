import chess

VALUES = {
    chess.PAWN: 100, 
    chess.KNIGHT: 320, 
    chess.BISHOP: 330, 
    chess.ROOK: 500, 
    chess.QUEEN: 900, 
    chess.KING: 20000
}

def evaluate(board):
    if board.is_checkmate():
        return -99999 if board.turn else 99999
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for sq in chess.SQUARES:
        p = board.piece_at(sq)
        if p:
            v = VALUES[p.piece_type]
            score += v if p.color == board.turn else -v
    return score

def alphabeta(board, depth, alpha, beta, maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    
    # Move Ordering: Prioritaskan langkah menangkap bidak terlebih dahulu
    moves = sorted(list(board.legal_moves), key=lambda m: board.is_capture(m), reverse=True)
    
    if maximizing:
        max_eval = -999999
        for m in moves:
            board.push(m)
            ev = alphabeta(board, depth - 1, alpha, beta, False)
            board.pop()
            if ev > max_eval:
                max_eval = ev
            if ev > alpha:
                alpha = ev
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 999999
        for m in moves:
            board.push(m)
            ev = alphabeta(board, depth - 1, alpha, beta, True)
            board.pop()
            if ev < min_eval:
                min_eval = ev
            if ev < beta:
                beta = ev
            if beta <= alpha:
                break
        return min_eval

def get_move(board: chess.Board) -> chess.Move:
    moves = sorted(list(board.legal_moves), key=lambda m: board.is_capture(m), reverse=True)
    if not moves:
        return None
    
    best_move = moves[0]
    best_val = -999999
    alpha = -999999
    beta = 999999
    
    # Depth 2 search dengan Alpha-Beta Pruning
    for m in moves:
        board.push(m)
        val = -alphabeta(board, 2, alpha, beta, False)
        board.pop()
        
        if val > best_val:
            best_val = val
            best_move = m
        if val > alpha:
            alpha = val

    return best_move
