import pygame

pygame.init()

tela = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Travessia Insper x FGV")

executando = True

while executando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            executando = False

pygame.quit()