from mancala import Board


def test_no_more_moves():
    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 1, 10, 1, 2, 3, 4, 5, 6]
    assert b.no_more_moves() == False

    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 0, 10, 1, 2, 3, 4, 5, 6]
    assert b.no_more_moves() == True

    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 1, 10, 0, 0, 0, 0, 0, 0]
    assert b.no_more_moves() == True


def test_heurestic():
    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 1, 10, 1, 2, 3, 4, 5, 6]
    assert b.get_heurestic_score() == -1
    assert b.get_opponent_board().get_heurestic_score() == -1


def test_player_points():
    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 1, 10, 1, 2, 3, 4, 5, 6]
    assert b.player_points == 10
    assert b.opponent_points == 11

    b = Board()
    b.board = [11, 0, 0, 0, 0, 0, 0, 10, 1, 2, 3, 4, 5, 6]
    assert b.player_points == 10
    assert b.opponent_points == 1 + 2 + 3 + 4 + 5 + 6 + 11

    b = Board()
    b.board = [11, 1, 2, 3, 4, 5, 6, 10, 0, 0, 0, 0, 0, 0]
    assert b.player_points == 1 + 2 + 3 + 4 + 5 + 6 + 10
    assert b.opponent_points == 11


def test_move():
    b = Board()
    cont = b.make_player_move(0)
    assert b.board == [0, 0, 5, 5, 5, 5, 4, 0, 4, 4, 4, 4, 4, 4]
    assert cont == False

    b = Board()
    cont = b.make_player_move(1)
    assert b.board == [0, 4, 0, 5, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4]
    assert cont == False

    b = Board()
    cont = b.make_player_move(2)
    assert b.board == [0, 4, 4, 0, 5, 5, 5, 1, 4, 4, 4, 4, 4, 4]
    assert cont == True

    b = Board()
    b.board = [0, 4, 4, 11, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4]
    cont = b.make_player_move(2)
    assert b.board == [0, 5, 4, 0, 6, 6, 6, 1, 5, 5, 5, 5, 5, 5]
    assert cont == False

    b = Board()
    b.board = [0, 4, 4, 13, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4]
    cont = b.make_player_move(2)
    assert b.board == [0, 5, 5, 0, 6, 6, 6, 7, 5, 5, 5, 0, 5, 5]
    assert cont == False


def test_possible_player_moves():
    b = Board()
    b.board = [0, 4, 0, 13, 5, 5, 5, 0, 4, 4, 4, 4, 4, 4]
    assert list(b.possible_player_moves()) == [0, 2, 3, 4, 5]


def test_get_moves():
    b = Board()
    moves = []
    b.get_player_moves(0, [], moves)
    assert [x[0] for x in moves] == [[0]]

    b = Board()
    moves = []
    b.get_player_moves(1, [], moves)
    assert [x[0] for x in moves] == [[1]]

    b = Board()
    moves = []
    b.get_player_moves(2, [], moves)
    assert set((tuple(x[0]) for x in moves)) == {(2, 0), (2, 1), (2, 3), (2, 4), (2, 5)}

    b = Board()
    b.board = [0, 0, 0, 0, 0, 2, 1, 0, 4, 4, 4, 4, 4, 4]

    moves = []
    b.get_player_moves(5, [], moves)
    assert set((tuple(x[0]) for x in moves)) == {(5, 4, 5)}

    b = Board()
    b.board = [0, 1, 0, 0, 0, 2, 1, 0, 4, 4, 4, 4, 4, 4]

    moves = []
    b.get_player_moves(5, [], moves)
    assert set((tuple(x[0]) for x in moves)) == {(5, 4, 5, 0), (5, 0), (5, 4, 0)}


def test_get_oponent_board():
    b = Board()
    b.board = [0, 5, 4, 0, 6, 6, 6, 1, 5, 5, 5, 5, 5, 5]
    assert b.get_opponent_board().board == [1, 5, 5, 5, 5, 5, 5, 0, 5, 4, 0, 6, 6, 6]


