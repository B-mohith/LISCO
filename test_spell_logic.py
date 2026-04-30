"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

import chess
from spell_logic import SpellChessGame, squares_in_3x3, squares_in_jump_range


# ------------------------------------------------------------------ #
#  Demo tests — provided to students as examples                      #
# ------------------------------------------------------------------ #

class TestFreezeTarget:
    """Casting Freeze should mark the opponent's color as frozen."""

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        # The frozen color should be Black (the opponent), not White
        assert game.freeze_effect_color == chess.BLACK


class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug — document it!                 #
# ------------------------------------------------------------------ #

class TestJumpCharges:
    """Each side beigns the game with 3 charges."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        whiteJumpCharges = game.jump_remaining[chess.WHITE]
        blackJumpCharges = game.jump_remaining[chess.BLACK]
        assert whiteJumpCharges == 3
        assert blackJumpCharges == 3

class TestJumpChargesNewGame:
    """Each side beigns the game with 3 charges when a new game is started."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.C3)
        game.new_game()
        whiteJumpCharges = game.jump_remaining[chess.WHITE]
        blackJumpCharges = game.jump_remaining[chess.BLACK]
        assert whiteJumpCharges == 3
        assert blackJumpCharges == 3

class TestJumpRange:
   """Verify range jump range is Chebyshev distance <= 2"""

   def test_jump_max_distance_2(self):
       # Center is e4 (file 4, rank 3)
       squares = squares_in_jump_range(chess.E4)
      
       # e6 (file 4, rank 5) -> distance 2 (valid)
       assert chess.E6 in squares
      
       # e7 (file 4, rank 6) -> distance 3 (invalid)
       # Spec: destination must be within Chebyshev distance 2
       assert chess.E7 not in squares
      
       # b7 (file 1, rank 6) -> distance 3 (invalid)
       assert chess.B7 not in squares

class TestJumpDestEmpty:
   """Verify that the piece can only land on an empty square - no capture can happen."""
  
   def test_jump_cannot_target_occupied_square(self):
       game = SpellChessGame()
       game.board.clear_board()
       game.board.turn = chess.WHITE
      
       # White piece at a1
       game.board.set_piece_at(chess.A1, chess.Piece(chess.KNIGHT, chess.WHITE))
       # Black piece at a3
       game.board.set_piece_at(chess.A3, chess.Piece(chess.PAWN, chess.BLACK))
      
       # Attempt to jump White Knight from a1 to a3 (occupied)
       success = game.cast_jump(chess.A1, chess.A3)
       assert success is False, "Jump should fail if destination square is occupied"

class TestJumpCooldown:
   """Verify that cooldown after casting is 2 turns."""
  
   def test_jump_cooldown_is_two_turns(self):
       game = SpellChessGame()
       game.board.clear_board()
       game.board.turn = chess.WHITE
      
       # White piece at c3
       game.board.set_piece_at(chess.C3, chess.Piece(chess.ROOK, chess.WHITE))
      
       game.cast_jump(chess.C3, chess.C4)
       
       # Spec says: "After casting Jump, the caster enters a 2-turn cooldown."
       assert game.jump_cooldown[chess.WHITE] == 2, f"Expected 2, got {game.jump_cooldown[chess.WHITE]}"
