import pygame
class ImageButton(object):

    def __init__(self,image,position,size,event_function):
        self._pos = position
        self._image = pygame.transform.scale(image,size) # size tuple
        self._event_function = event_function
        self._rect = pygame.Rect(self._pos, size)

    def draw(self, screen):

        # draw selected image
        screen.blit(self._image, self._pos)

    def event_handler(self, event):

        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    self._event_function()

class PieceButton(object):

    def __init__(self,image,image_bw,position,size,event_function = lambda: None):
        self._pos = position
        self._image = pygame.transform.scale(image,size) # size tuple
        self._image_bw = pygame.transform.scale(image_bw,size) # size tuple
        self._event_function = event_function
        self._rect = pygame.Rect(self._pos, size)
        self._active = True

    def draw(self, screen):

        # draw selected image
        if self._active:
            screen.blit(self._image, self._pos)
        else:            
            screen.blit(self._image_bw, self._pos)

    def set_inactive(self):
        self._active = False
    def set_active(self):
        self._active = True

    def event_handler(self, event):

        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    self._event_function()

class TurnButton(object):

    def __init__(self,image_red,image_black,position,size,turn,event_function):
        self._pos = position
        self._image_red = pygame.transform.scale(image_red,size) # size tuple
        self._image_black = pygame.transform.scale(image_black,size) # size tuple
        self._event_function = event_function
        self._rect = pygame.Rect(self._pos, size)
        self._active = True
        self._turn = turn

    def draw(self, screen):

        # draw selected image
        if self._turn == "red":
            screen.blit(self._image_red, self._pos)
        else:            
            screen.blit(self._image_black, self._pos)

    def set_red(self):
        self._turn = "red"
    def set_black(self):
        self._turn = "black"

    def change_turn(self):
        if self._turn == "red":
            self.set_black()
        else:
            self.set_red()
    def event_handler(self, event):
        # change selected color if rectange clicked
        if event.type == pygame.MOUSEBUTTONDOWN: # is some button clicked
            if event.button == 1: # is left button clicked
                if self._rect.collidepoint(event.pos): # is mouse over button
                    
                    self._event_function()