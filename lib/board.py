# -*- encoding: utf-8 -*-
import pygame
import utils


class Board:
    "Representa el tablero donde se muestran las fichas"

    def __init__(self, gamescene):
        self.pieces = []
        self.matrix = self.init_matrix(10, 18)
        self.gamescene = gamescene

    def update(self):
        pass

    def draw_block(self, row, col, screen):
        # TODO: posicionar correctamente el rectangulo en
        #       base a la posicion del tablero.
        color = (200, 200, 0)
        screen.fill(color, (col * 20, row * 20, 20, 20))

    def draw(self, screen):
        # TODO: leer la matriz de colisiones y dibujar un bloque
        #       cada celda con 1 (colisionable)
        
        #self.draw_block(10, 10, screen)
        pass

    def init_matrix(self, cells_width, cells_height):
        board = []

        for y in range(cells_height):
            line = []

            for x in range(cells_width):
                line.append(0)

            board.append(line)

        return board

    def can_put_this_piece_here(self, row, col, mask):
        """Informa si una pieza se puede colocar en una determinada posición.

        Este método evalua las colisiones de una pieza ante un posible
        movimiento."""

        for delta_row in range(0, 4):
            for delta_column in range(0, 4):

                if mask[delta_row][delta_column]:
                    dst_col = col - 1 + delta_column
                    dst_row = row - 1 + delta_row

                    if dst_col < 0:
                        return False

                    try:
                        if self.matrix[dst_row][dst_col]:
                            return False
                    except IndexError:
                        return False

        return True

    def put_one_piece_here(self, row, col, mask):
        for delta_row in range(0, 4):
            for delta_column in range(0, 4):

                if mask[delta_row][delta_column]:
                    dst_col = col - 1 + delta_column
                    dst_row = row - 1 + delta_row

                    self.matrix[dst_row][dst_col] = mask[delta_row][delta_column]

        print "Asi queda la matriz luego de colocar la pieza."
        import pprint
        pprint.pprint(self.matrix)

    def go_to_next_piece(self):
        self.gamescene.go_to_next_scene()
