import unittest
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Array import convert_fen_to_board, get_color
from ai.Minimax_array import minimax

#Test if Minimax with AlphaBeta gets the best Move (Projekt Wiki)

class TestAlphaBeta(unittest.TestCase):
    def test_alphabeta(self):
        test_cases = [
                {
                    "fen": '1bb4/1b0b05/b01b0bb4/1b01b01b02/3r01rr2/b0r0r02rr2/4r01rr1/4r0r0 b',
                    "bester_move": (('A', 6),('A', 7)),
                    "group": "GroupH"
                },
                {
                    "fen": '6/3b0b03/3r02bb1/b0b03bb2/rrrr1bb2rr1/2b01b01r01/2r01r02r0/4r01 b',
                    "bester_move": (('D', 5),('C', 7)),
                    "group": "GroupH"
                },
                {
                    "fen": '6/3b0b03/3r02bb1/b0b03bb2/rrrr1bb2rr1/2b01b01r01/2r01r02r0/4r01 r',
                    "bester_move": (('D', 3),('E', 2)),
                    "group": "GroupH"
                },
                {
                    "fen": '6/7b0/8/8/1r06/4b03/2rr1rrr02/5r0 b',
                    "bester_move": (('E', 6),('D', 6)),
                    "group": "GroupF"
                },
                {
                    "fen": '6/4bbb02/b02b01b02/1b02b03/2b01rrrr2/6r01/r01r0r0r03/5r0 r',
                    "bester_move": (('E', 5),('D', 3)),
                    "group": "GroupF"
                },
                {
                    "fen": '1b0b0b02/8/3b04/3b04/r0r06/2b05/5r0r01/6 b',
                    "bester_move": (('C', 6),('C', 7)),
                    "group": "GroupT"
                },
                {
                    "fen": '6/4bb3/8/8/4b0r0b01/8/8/6 b',
                    "bester_move": (('E', 2),('F', 4)),
                    "group": "GroupT"
                },
                {
                    "fen": '3b02/5b02/8/1b06/4bb3/6r01/1r06/1r0r03 b',
                    "bester_move": (('E', 5),('F', 7)),
                    "group": "GroupI"
                },
                {
                    "fen": '6/1b06/5b02/2b05/2b05/4r03/2r05/6 b',
                    "bester_move": (('C', 4),('C', 5)),
                    "group": "GroupI"
                }

            ]
        for index, case in enumerate(test_cases, start=1):
            with self.subTest(case=case):
                fen_string = case["fen"]
                bester_move = case["bester_move"]
                group_name = case["group"]
                board = convert_fen_to_board(fen_string)
                color = get_color(fen_string)
                print(f"Testing case {index} from {group_name} with FEN: {fen_string}")
                try: 
                    x = minimax(board, '', 3, float('-inf'), float('inf'), True, color)
                    our_move = x[1]
                    self.assertEqual(our_move, bester_move, f"Failed for {group_name} FEN: {fen_string}")
                except Exception as e:
                    self.fail(f"Exception for {group_name} FEN: {fen_string} with error: {e}")
            
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(TestAlphaBeta('test_alphabeta'))
    return suite

if __name__ == '__main__':
    unittest.main()     

#RUN 