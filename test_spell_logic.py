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

    def test_jump_charges(self):
        game = SpellChessGame()
        whiteJumpCharges = game.jump_remaining[chess.WHITE]
        blackJumpCharges = game.jump_remaining[chess.BLACK]
        assert whiteJumpCharges == 3
        assert blackJumpCharges == 3

class TestJumpChargesNewGame:
    """Each side beigns the game with 3 charges when a new game is started."""

    def test_jump_charges_new_game(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.C3)
        game.new_game()
        whiteJumpCharges = game.jump_remaining[chess.WHITE]
        blackJumpCharges = game.jump_remaining[chess.BLACK]
        assert whiteJumpCharges == 3
        assert blackJumpCharges == 3

# Freeze tests for Sprint 1a, 1b, 1c
class TestFreezeCharges: # 1a
    """Each side beigns the game with 5 Freeze charges.
        This class tests that the charges decrement or are set 
        appropriately. """

    def test_charges(self):
        game = SpellChessGame()
        whiteFreezeCharges = game.freeze_remaining[chess.WHITE]
        blackFreezeCharges = game.freeze_remaining[chess.BLACK]
        assert whiteFreezeCharges == 5
        assert blackFreezeCharges == 5

class TestFreezeChargesOnUseWhite:
    """This class tests that the charges decrement or are set 
        appropriately. """
    
    def test_charge_after_spell_use_white(self):
        game = SpellChessGame()
        # white casts freeze 
        game.cast_freeze(chess.D4)
        # get remaining freeze charges
        whiteFreezeCharges = game.freeze_remaining[chess.WHITE]
        blackFreezeCharges = game.freeze_remaining[chess.BLACK]
        # white should have 1 less charge for freeze
        assert whiteFreezeCharges == 4
        assert blackFreezeCharges == 5

class TestFreezeChargesOnUseBlack:
    """This class tests that the charges decrement or are set 
        appropriately. """
    
    def test_charge_after_spell_use_black(self):
        game = SpellChessGame()
        # white moves
        game.make_move(chess.E2, chess.E4)
        # black casts freeze
        game.cast_freeze(chess.E4)
        # get remaining freeze charges
        whiteFreezeCharges = game.freeze_remaining[chess.WHITE]
        blackFreezeCharges = game.freeze_remaining[chess.BLACK]
        # white should have 1 less charge for freeze
        assert whiteFreezeCharges == 5
        assert blackFreezeCharges == 4 

class TestFreezeChargesOnGameReset:
    """This class tests if freeze charges are correctly set to 5
        per player when a new game is reset."""
    def test_charges_on_new_game(self):
        game = SpellChessGame()
        game.cast_freeze(chess.D4)
        game.new_game()
        whiteFreezeCharges = game.freeze_remaining[chess.WHITE]
        blackFreezeCharges = game.freeze_remaining[chess.BLACK]
        assert whiteFreezeCharges == 5
        assert blackFreezeCharges == 5

class TestFreezeDisplay():
    pass 

class TestJumpChargesCost:
    """Each Jump spell cast should cost 1 charge."""

    def test_jump_charges_cost(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.C3)
        whiteJumpCharges = game.jump_remaining[chess.WHITE]
        assert whiteJumpCharges == 2

class TestJumpZeroCharges:
    """When a player has 0 charges remaining, they cannot cast Jump."""

    def test_jump_zero_charges(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.B2)
        game.make_move(chess.E7, chess.E6)
        game.make_move(chess.A1, chess.A2)
        game.make_move(chess.D7, chess.D6)
        game.make_move(chess.C1, chess.C2)
        game.make_move(chess.A7, chess.A6)
        game.cast_jump(chess.D1, chess.D2)
        game.make_move(chess.A6, chess.A5)
        game.make_move(chess.D2, chess.D3)
        game.make_move(chess.A5, chess.A4)
        game.make_move(chess.D3, chess.D4)
        game.make_move(chess.A4, chess.A3)
        game.cast_jump(chess.D4, chess.D5)
        game.make_move(chess.E6, chess.E5)
        game.make_move(chess.D5, chess.D6)
        game.make_move(chess.E5, chess.E4)
        game.make_move(chess.B2, chess.B3)
        game.make_move(chess.E4, chess.E3)
        game.cast_jump(chess.B3, chess.B4)
        ans = game.jump_casted_this_turn
        assert ans == False

class TestFreezeLegalMoves:
    """Verifies that pieces in the frozen area cannot move."""

    def test_frozen_pieces_not_in_legal_moves(self):
        game = SpellChessGame()
        # cast freeze
        game.cast_freeze(chess.E5)
        # apply freeze (need a move)
        game.make_move(chess.E2, chess.E4)
        # get legal moves
        legal_moves = game.get_legal_moves()
        # squares affected by freeze
        frozen_squares = squares_in_3x3(chess.E5)
        # check that no move originates from frozen squares
        for move in legal_moves:
            assert move.from_square not in frozen_squares

class TestFreezeDuration:
    """Verifies that Freeze effect expires after a certain duration."""

    def test_freeze_duration_expires(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        #apply freeze
        game.make_move(chess.E2, chess.E4)
        #freeze should be active
        assert game.freeze_effect_plies_left == 1
        #simulate turns
        game.make_move(chess.E7, chess.E5)
        game.make_move(chess.G1, chess.F3)
        #freeze should expire
        assert game.freeze_effect_color is None

class TestFreezeCooldown:
    """Verifies that Freeze cooldown decreases after each turn."""

    def test_freeze_cooldown_decrements(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        start_cd = game.freeze_cooldown[chess.WHITE]
        #simulate turns
        game.make_move(chess.E2, chess.E4)
        # Cooldown should not decrease on opponent's turn
        assert game.freeze_cooldown[chess.WHITE] == start_cd
        # Black moves, then it becomes White's turn again
        game.make_move(chess.E7, chess.E5)
        #cooldown should decrease
        assert game.freeze_cooldown[chess.WHITE] == start_cd - 1

class TestFreezeOnlyAffectsOpponent:
    """Verify Freeze Only Affects Opponent"""

    def test_freeze_does_not_affect_caster(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        # white move
        game.make_move(chess.E2, chess.E4)
        # E4 is inside the 3x3 freeze area centered on E5,
        # but White is the caster, so White should not be frozen.
        assert not game.is_frozen(chess.E4, chess.WHITE)

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

class TestJumpOwnPiece:
    """To cast, the player must select one of their own pieces"""

    def test_jump_own_piece(self):
        game = SpellChessGame()
        game.cast_jump(chess.B7, chess.C3)
        ans = game.jump_casted_this_turn
        assert ans == False

class TestJumpEmptySquare:
    """While casting a Jump, the destination square must be empty"""

    def test_jump_empty_square(self):
        game = SpellChessGame()
        game.cast_jump(chess.B1, chess.A1)
        ans = game.jump_casted_this_turn
        assert ans == False

class TestJumpKing:
    """The Jump spell cannot be casted on King"""

    def test_jump_king(self):
        game = SpellChessGame()
        game.cast_jump(chess.E1, chess.E3)
        ans = game.jump_casted_this_turn
        assert ans == False
class TestJumpTeleport:
    """The Jump spell cannot be casted on King"""

    def test_jump_teleport(self):
        game = SpellChessGame()
        piece1 = game.board.piece_at(chess.D1)
        game.cast_jump(chess.D1, chess.E3)
        piece2 = game.board.piece_at(chess.E3)
        assert piece1 == piece2