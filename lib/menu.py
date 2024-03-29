# -*- encoding: utf-8 -*-
import pygame
import utils
import pytweener


class Cursor:

    def __init__(self, start_y, item_height, initial_selected):
        self.image, self.rect = utils.load_images("cursor.png")
        self.rect.centerx = 320
        self.start_y = start_y
        self.y = 0
        self.item_height = item_height
        self.tweener = pytweener.Tweener()

        self.set_position(initial_selected)

    def on_draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_position(self, index, inmediately=False):
        to_y = self.start_y + index * self.item_height - 2
        if not inmediately:
            self.tweener.addTween(self, y=to_y, tweenTime=0.5)
        else:
            self.y = to_y

    def on_update(self):
        self.tweener.update(0.1)
        self.rect.y = self.y


class Menu:
    "Representa un menu dentro del juego, por ejemplo el menu principal."

    def __init__(self, options, initial_selected=0):
        self.options = options

        selected_font = utils.load_font("FreeSans.ttf", 30)
        selected_color = (255, 255, 255)
        font = utils.load_font("FreeSans.ttf", 30)
        color = (0, 0, 0)

        self.normal_font = font
        self.normal_color = color
        self.selected_font = selected_font
        self.selected_color = selected_color
        self.start_y = 200
        self.item_height = 50

        self.cursor = Cursor(self.start_y, self.item_height, initial_selected)
        
        self.selected = initial_selected
        self.imgs_normal = []
        self.imgs_selected = []
        
        self._create_option_images()
        self.last_mouse_position = pygame.mouse.get_pos()
        # espera unos segundos antes de que el usuario pueda seleccionar algo
        self.delay = 50

    def on_update(self):
        self.cursor.on_update()
        self.handle_mouse_motion()

        if pygame.mouse.get_pressed()[0]:
            self.do_select()

        if self.delay > 0:
            self.delay -= 1


    def handle_mouse_motion(self):
        new_mouse_position = pygame.mouse.get_pos()

        if self.last_mouse_position != new_mouse_position:
            self.last_mouse_position = new_mouse_position 
            self._change_cursor_position_by_mouse(new_mouse_position)

    def _change_cursor_position_by_mouse(self, position):
        mouse_x, mouse_y = position

        for i in range(len(self.options)):
            if i == self.selected:
                img = self.imgs_selected[i]
            else:
                img = self.imgs_normal[i]
            
            x = 100
            y = self.start_y + i * self.item_height
            w = 440
            h = 50
            
            rect = pygame.Rect((x, y, w, h))

            if rect.collidepoint(mouse_x, mouse_y):
                self.set_select_position(i)


    def _create_option_images(self):
        "Genera todos los items del menú."
        line_step = 0

        for (text, callback) in self.options:
            img_normal, img_normal_size = utils.render_text(text, self.normal_font, 
                    self.normal_color)
            img_selected, img_selected_size = utils.render_text(text, 
                    self.selected_font, self.selected_color)
            
            self.imgs_normal.append(img_normal)
            self.imgs_selected.append(img_selected)
            
            line_step = max(max(img_normal_size[3], img_selected_size[3]), line_step)
        
        self.line_step = line_step
    
    def on_draw(self, screen):
        "Dibuja todos los items y el cursor."
        center_x = screen.get_width() / 2
        
        self.cursor.on_draw(screen)

        for i in range(len(self.options)):
            if i == self.selected:
                img = self.imgs_selected[i]
            else:
                img = self.imgs_normal[i]
            
            x = center_x - img.get_width() / 2
            y = self.start_y + i * self.item_height
            
            screen.blit(img, (x,y))

    def prev(self):
        "Regresa una opcion para arriba."
        self.selected = (self.selected - 1) % len(self.options)
        self.cursor.set_position(self.selected)
    
    def next(self):
        "Avanza a la siguiente opcion."
        self.selected = (self.selected + 1) % len(self.options)
        self.cursor.set_position(self.selected)

    def set_select_position(self, index):
        self.selected = (index) % len(self.options)
        self.cursor.set_position(self.selected, True)

    def do_select(self):
        "Cuando seleccionan pulsado ENTER o similar."
        (title, callback) = self.options[self.selected]

        if self.delay <= 0:
            callback()
            self.delay = 50
