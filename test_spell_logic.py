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

class TestFreezeZeroCharges:
    """ This class tests that a player cannot use freeze if they have 0 charges remaining"""

    def test_freeze_zero_charges(self):
        game = SpellChessGame()
        for i in range(5):
            freeze_cast = game.cast_freeze(chess.G7) # freeze is casted, 3 turn cooldown
            game.make_move(chess.B1, chess.C3) # 1 turn passed
            game.make_move(chess.B8, chess.C6) 
            game.make_move(chess.C3, chess.B1) # 2 turn 
            game.make_move(chess.C6, chess.B8)
            game.make_move(chess.B1, chess.C3) # 3 turn passed
            game.make_move(chess.B8, chess.C6) 

        freeze_cast = game.cast_freeze(chess.G7)
        assert freeze_cast == False

class TestFreezeCastFailBeforeCooldown:
    """ This class tests that a player cannot use freeze if casted freeze 3 turns ago"""

    def test_freeze_cast_one_turn(self):
        game = SpellChessGame()
        freeze_cast = game.cast_freeze(chess.G7) # freeze is casted, 3 turn cooldown
        game.make_move(chess.A2, chess.A3) # 1 turn passed 
        game.make_move(chess.A7, chess.A6) 
        freeze_cast = game.cast_freeze(chess.G7) # 2nd freeze
        assert freeze_cast == False

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
        assert game.freeze_effect_plies_left > 0
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
        game.make_move(chess.E7, chess.E5)
        #cooldown should decrease
        assert game.freeze_cooldown[chess.WHITE] < start_cd
