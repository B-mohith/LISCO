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
    """"""