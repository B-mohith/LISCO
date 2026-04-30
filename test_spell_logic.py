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
    
