import pygame

def load_images(theme):
    return {
        '#': pygame.image.load('./themes/' + theme + '/images/wall.png').convert(),
        ' ': pygame.image.load('./themes/' + theme + '/images/space.png').convert(),
        '$': pygame.image.load('./themes/' + theme + '/images/box.png').convert(),
        '.': pygame.image.load('./themes/' + theme + '/images/goal.png').convert(),
        '@': pygame.image.load('./themes/' + theme + '/images/player.png').convert(),
        '*': pygame.image.load('./themes/' + theme + '/images/box_on_goal.png').convert(),
    }
