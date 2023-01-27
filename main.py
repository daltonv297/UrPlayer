from graphics import *
import numpy as np
import math

WIDTH = 1024
HEIGHT = 768

def rotate(origins, points, angle):
    diff = points - origins

    rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

    return origins + diff @ rot_matrix.T

# def get_square_centers(square_size):



class Player:
    def __init__(self, side, color, is_human=True):
        self.side = side
        self.color = color
        self.piece_locs = [0] * 16
        self.piece_locs[0] = 7
        self.is_human = is_human


class Game:
    def __init__(self):
        self.player1 = Player('left', 'blue')
        self.player2 = Player('right', 'red')
        self.current_turn = np.random.choice([self.player1, self.player2])


class BoardGraphics:
    def __init__(self, win, square_size, game):
        self.win = win
        self.square_size = square_size
        self.game = game
        self.center_points = None
        self.piece_objects = []
        self.piece_rad = square_size * 0.35

        self.text = {}

    def draw_board(self):
        l_x = self.win.getWidth()
        l_y = self.win.getHeight()

        center_x = l_x / 2
        center_y = l_y / 2

        grid_width = 3 * self.square_size
        grid_height = 8 * self.square_size
        xx, yy = np.meshgrid(np.arange(0, grid_width, self.square_size), np.arange(0, grid_height, self.square_size))

        grid_center_x = grid_width / 2
        grid_center_y = grid_height / 2

        xx += int(center_x - grid_center_x)
        yy += int(center_y - grid_center_y)

        corner_coords = np.array([[Point(x, y) for x, y in zip(row_x, row_y)] for row_x, row_y in zip(xx, yy)])

        nosquares = np.array([[4, 0], [5, 0], [4, 2], [5, 2]]).T
        corner_coords[nosquares[0], nosquares[1]] = None

        for row in corner_coords:
            for p in row:
                if p is not None:
                    Rectangle(p, Point(p.getX() + self.square_size, p.getY() + self.square_size)).draw(self.win)

        self.center_points = np.array(
            [[[x + self.square_size / 2, y + self.square_size / 2] for x, y in zip(row_x, row_y)] for row_x, row_y in
             zip(xx, yy)])

        star_inds = np.array([[0, 0], [6, 0], [0, 2], [6, 2], [3, 1]]).T

        star_coords = self.center_points[star_inds[0], star_inds[1]]

        star_size = 50
        num_rots = 3
        angles = np.radians(np.arange(0, 360, 360 / num_rots))

        for a in angles:
            poly_points = np.empty((0, 5, 2))
            poly_points = np.append(poly_points, [star_coords + np.array([1, 1]) * star_size / 2], axis=0)
            poly_points = np.append(poly_points, [star_coords + np.array([-1, 1]) * star_size / 2], axis=0)
            poly_points = np.append(poly_points, [star_coords + np.array([-1, -1]) * star_size / 2], axis=0)
            poly_points = np.append(poly_points, [star_coords + np.array([1, -1]) * star_size / 2], axis=0)

            poly_points_rotated = np.empty((0, 5, 2))
            for point in poly_points:
                poly_points_rotated = np.append(poly_points_rotated, [rotate(star_coords, point, a)], axis=0)

            poly_points_rotated = np.transpose(poly_points_rotated, (1, 0, 2))

            for poly in poly_points_rotated:
                Polygon(*[Point(*p) for p in poly]).draw(self.win)

        self.text['pieces_remaining_1'] = Text(Point(200, 200), str(self.game.player1.piece_locs[0]))
        self.text['pieces_remaining_2'] = Text(Point(l_x-200, 200), str(self.game.player2.piece_locs[0]))
        self.text['score_1'] = Text(Point(200, 600), str(self.game.player1.piece_locs[-1]))
        self.text['score_2'] = Text(Point(l_x-200, 600), str(self.game.player2.piece_locs[-1]))

        for t in self.text.values():
            t.setSize(30)
            t.draw(self.win)



    def get_piece_coords(self, player):
        if player.side == 'left':
            coord_map = np.array([[3, 0], [2, 0], [1, 0], [0, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1],
                                  [6, 1], [7, 1], [7, 0], [6, 0]])
        else:
            coord_map = np.array([[3, 2], [2, 2], [1, 2], [0, 2], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1],
                                  [6, 1], [7, 1], [7, 2], [6, 2]])

        piece_mask = np.array(player.piece_locs[1:-1]) > 0
        active_squares = coord_map[piece_mask]
        active_squares = active_squares.T
        return self.center_points[active_squares[0], active_squares[1]]

    def update_board(self):
        for obj in self.piece_objects:
            obj.undraw()
        self.piece_objects = []

        for player in (self.game.player1, self.game.player2):
            piece_locs = self.get_piece_coords(player)
            for loc in piece_locs:
                piece = Circle(Point(*loc), self.piece_rad)
                piece.setFill(player.color)
                piece.draw(self.win)
                self.piece_objects.append(piece)

        self.text['pieces_remaining_1'].setText(str(self.game.player1.piece_locs[0]))
        self.text['pieces_remaining_2'].setText(str(self.game.player2.piece_locs[0]))
        self.text['score_1'].setText(str(self.game.player1.piece_locs[-1]))
        self.text['score_2'].setText(str(self.game.player2.piece_locs[-1]))



def main():

    win = GraphWin('testwin', WIDTH, HEIGHT, autoflush=False)
    square_size = 80
    game = Game()
    board = BoardGraphics(win, square_size, game)
    board.draw_board()

    while True:
        game.player1.piece_locs = [4, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5]
        game.player2.piece_locs = [2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3]

        board.update_board()

        #win.getMouse()
        update(10)

        game.player1.piece_locs = [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1]
        game.player2.piece_locs = [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]

        board.update_board()
        update(10)

    #win.getMouse()


if __name__ == '__main__':
    main()
