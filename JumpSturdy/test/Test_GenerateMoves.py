import unittest
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Array import convert_fen_to_board, get_color, generate_moves
#Test if generate moves gets the right amount of Moves (Projekt Wiki)

class TestGenerateMoves(unittest.TestCase):
    def test_generate_moves(self):
        test_cases = [
                {
                    "fen": '6/1b06/1r03bb2/2r02b02/8/5r0r01/2r0r04/6 r',
                    "expected_moves": 17,
                    "group": "GroupA"
                },
                {
                    "fen": '6/1b0b0b0b0b0b01/1b0b0b0b0b0b01/8/8/1r0r0r0r0r0r01/1r0r0r0r0r0r01/6 b',
                    "expected_moves": 36,
                    "group": "GroupA"
                },
                 {
                    "fen": 'b0b0b02bb/1b01b0bb1b01/2b05/5b02/1r06/8/2r0rrr0rr1r0/rr2r01r0 b',
                    "expected_moves": 28,
                    "group": "GroupI"
                },
                 {
                    "fen": 'bb4bb/3b02b01/r07/2r02r02/4b03/2b02r02/2r01r01r0r0/1r01r02 r',
                    "expected_moves": 28,
                    "group": "GroupI"
                },
                   {
                    "fen": 'b0b01b0b0b0/1b0b02b0b01/3b0b03/2b05/3r04/2r05/1r01rr1r0r01/r0r02r0r0 b',
                    "expected_moves": 35,
                    "group": "GroupO"
                },
                 {
                    "fen": '6/2bb1b03/5b02/3b01r02/2b05/8/1rr1r02r01/6 r',
                    "expected_moves": 11,
                    "group": "GroupO"
                },
                {
                    "fen": '6/8/5r02/8/8/8/r0b0r05/r05 b',
                    "expected_moves": 0,
                    "group": "Jessica(Forum)"
                }

            ]
        for index, case in enumerate(test_cases, start=1):
            fen_string = case["fen"]
            expected_moves = case["expected_moves"]
            group_name = case["group"]
            board = convert_fen_to_board(fen_string)
            color = get_color(fen_string)
            moves = generate_moves(board, color)
            self.assertEqual(len(moves), expected_moves, f"Failed for {group_name} FEN: {fen_string}")
            
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    suite.addTest(TestGenerateMoves('test_generate_moves'))
    return suite

if __name__ == '__main__':
    unittest.main()

#RUN    