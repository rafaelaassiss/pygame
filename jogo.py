import pygame

# --------------------------------------------------
# CONFIGURAÇÕES INICIAIS
# --------------------------------------------------

# Resolução lógica do jogo.
# O Pygame vai ampliar essa resolução para ocupar a tela inteira.
LARGURA = 1000
ALTURA = 700


# --------------------------------------------------
# CORES
# --------------------------------------------------

FUNDO = (245, 243, 235)
TEXTO = (37, 48, 58)

AZUL = (48, 115, 150)
AZUL_CLARO = (203, 227, 234)

VERDE = (32, 119, 99)
LARANJA = (213, 133, 59)

BRANCO = (255, 255, 255)
CINZA = (220, 220, 214)
PRETO = (0, 0, 0)

VERMELHO = (173, 71, 67)


# --------------------------------------------------
# INICIALIZAÇÃO DO PYGAME
# --------------------------------------------------

pygame.init()


# Cria a tela cheia.
# 1000 x 700 continua sendo a resolução usada pelo código
# para posicionar os elementos.
tela = pygame.display.set_mode(
    (LARGURA, ALTURA),
    pygame.FULLSCREEN | pygame.SCALED
)

pygame.display.set_caption("Travessia Insper x FGV")


# Controla a quantidade de quadros por segundo.
relogio = pygame.time.Clock()


# --------------------------------------------------
# LOOP PRINCIPAL
# --------------------------------------------------

executando = True

while executando:

    # Percorre todos os eventos que aconteceram.
    for evento in pygame.event.get():

        # Fecha o jogo pelo botão de fechar.
        if evento.type == pygame.QUIT:
            executando = False

        # Verifica teclas pressionadas.
        if evento.type == pygame.KEYDOWN:

            # ESC fecha o jogo.
            if evento.key == pygame.K_ESCAPE:
                executando = False


    # Preenche a tela com uma cor enquanto
    # ainda não construímos o cenário.
    tela.fill(FUNDO)


    # Atualiza o que aparece na tela.
    pygame.display.flip()


    # Limita o jogo a 60 FPS.
    relogio.tick(60)


# --------------------------------------------------
# ENCERRAMENTO
# --------------------------------------------------

pygame.quit()