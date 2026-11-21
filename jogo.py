import io
import random
import math
import struct
import wave
import pygame
import csv
from pathlib import Path

LARGURA = 1000
ALTURA = 700
NOMES_FASE1 = ["Insper 1", "Insper 2", "Insper 3", "FGV 1", "FGV 2", "FGV 3"]
NOMES_FASE2 = ["Insper 1", "Insper 2", "Insper 3", "Insper 4",
               "FGV 1", "FGV 2", "FGV 3", "FGV 4"]

def nome_personagem(numero, fase):
    if fase == 1:
        return NOMES_FASE1[numero - 1]
    return NOMES_FASE2[numero - 1]

FALAS = [
    "Isso conta como atividade complementar?",
    "Meu terno não pode molhar!",
    "Essa viagem tem certificado?",
    "O remo entra como experiência profissional?",
    "Já coloquei capitão no currículo.",
    "Tem café nessa reunião flutuante?",
    "Podemos chamar isso de intercâmbio?",
    "Vou abrir uma startup de barcos.",
    "Isso aumenta meu networking, né?"
]

FUNDO = (245, 243, 235)
TEXTO = (37, 48, 58)
AZUL = (48, 115, 150)
AZUL_CLARO = (203, 227, 234)
VERDE = (32, 119, 99)
LARANJA = (213, 133, 59)
BRANCO = (255, 255, 255)
CINZA = (220, 220, 214)
VERMELHO = (173, 71, 67)

def criar_audio(notas, duracao = 0.2, volume = 0.1, baixo = False):
  """Gera uma pequena música/efeito em WAV sem depender de arquivos externos."""
  taxa = 22050
  dados = bytearray()

  for frequencia in notas:
    quantidade = int(taxa * duracao)
    for indice in range(quantidade):
      tempo = indice / taxa
      if frequencia == 0:
        onda = 0
      else:
        onda = math.sin(2 * math.pi * frequencia * tempo)
        onda += 0.3 * math.sin(2 * math.pi * frequencia * 2 * tempo)
        if baixo:
          onda += 0.22 * math.sin(2 * math.pi * (frequencia / 2) * tempo)
        onda /= 1.52
      parte = indice / quantidade
      envelope = min(1, parte / 0.08, (1 - parte) / 0.12)
      onda *= max(0, envelope)
      valor = int(max(-1, min(1, onda * volume)) * 32767)
      dados.extend(struct.pack("<h", valor))
  
  arquivo = io.BytesIO()
  wav = wave.open(arquivo, "wb")
  wav.setnchannels(1)
  wav.setsampwidth(2)
  wav.setframerate(taxa)
  wav.writeframes(bytes(dados))
  wav.close()
  return arquivo.getvalue()

def criar_trilha_menu():
  return criar_audio([261.63, 329.63, 392.00, 493.88, 392.00, 329.63,
                        293.66, 349.23, 440.00, 523.25, 440.00, 349.23],
                       0.24, 0.085, True)
  
def criar_trilha_fase1():
  return criar_audio([220.00, 261.63, 329.63, 392.00, 329.63, 261.63,
                        246.94, 293.66, 349.23, 440.00, 349.23, 293.66],
                       0.18, 0.075, True)
  
def criar_trilha_fase2():
  return criar_audio([392.00, 493.88, 587.33, 783.99], 0.13, 0.13, False)
  
def criar_som_vitoria():
  return criar_audio([392.00, 493.88, 587.33, 783.99], 0.13, 0.13, False)
  
def criar_som_derrota():
  return criar_audio([329.63, 293.66, 246.94, 196.00, 146.83], 0.16, 0.11, True)
  
def desenhar_texto(tela, texto, fonte, cor, x, y, centralizado = False):
  """Transforma uma frase em imagem e coloca essa imagem na janela."""
  imagem = fonte.render(texto, True, cor)

  if centralizado:
    x = x - imagem.get_width() // 2
    y = y - imagem.get_height() // 2
  tela.blit(imagem, (x, y))
  
def ponto_dentro(posicao, area):
  """Verifica se o clique está dentro dos limites de um botão ou aluno."""
  x, y = posicao
  area_x, area_y, largura, altura = area

  if x >= area_x and x <= area_x + largura:
    if y >= area_y and y <= area_y + altura:
      return True
  return False

def desenhar_botao(tela, texto, area, fonte, mouse):
  """Desenha o botão e muda a cor quando o mouse passar sobre ele."""
  x, y, largura, altura = area

  if ponto_dentro(mouse, area):
    cor = (45, 45, 45)
  else:
    cor = (0, 0, 0)
  pygame.draw.rect(tela, cor, (x, y, largura, altura), border_radius = 12)
  desenhar_texto(tela, texto, fonte, BRANCO, x + largura // 2, y + altura // 2, True)

# ---------------- ETAPA 4: PERSONAGENS E GRUPOS ----------------
def contar_grupos(margem, fase):
    """Conta raposas do Insper e jacarés da FGV de acordo com a fase."""
    limite = 3 if fase == 1 else 4
    quantidade_insper = 0
    quantidade_fgv = 0

    for numero in margem:
        if numero <= limite:
            quantidade_insper = quantidade_insper + 1
        else:
            quantidade_fgv = quantidade_fgv + 1

    return quantidade_insper, quantidade_fgv

def desenhar_personagem(tela, numero, x, y, fase):
    """Desenha raposas do Insper e jacarés da FGV com ternos e gravatas."""
    limite = 3 if fase == 1 else 4
    cores_raposas = [(222, 117, 46), (194, 91, 35), (239, 148, 67), (205, 105, 42)]
    cores_jacares = [(76, 145, 75), (54, 122, 81), (102, 159, 82), (70, 135, 70)]

    if numero <= limite:
        gravata = (190, 45, 58)
        terno = (48, 51, 65)
        pele = cores_raposas[numero - 1]
    else:
        gravata = (43, 112, 195)
        terno = (28, 49, 78)
        pele = cores_jacares[numero - limite - 1]

    # Cauda, pernas e sapatos sociais.
    if numero <= limite:
        pygame.draw.polygon(tela, pele, [(x + 32, y + 55), (x + 48, y + 44),
                                        (x + 44, y + 67), (x + 32, y + 66)])
        pygame.draw.polygon(tela, BRANCO, [(x + 48, y + 44), (x + 44, y + 67),
                                          (x + 39, y + 60)])
    else:
        pygame.draw.polygon(tela, pele, [(x + 32, y + 54), (x + 48, y + 69),
                                        (x + 31, y + 67)])
    pygame.draw.line(tela, terno, (x + 15, y + 62), (x + 13, y + 89), 9)
    pygame.draw.line(tela, terno, (x + 27, y + 62), (x + 29, y + 89), 9)
    pygame.draw.ellipse(tela, TEXTO, (x + 3, y + 85, 18, 9))
    pygame.draw.ellipse(tela, TEXTO, (x + 24, y + 85, 18, 9))

    # Mesmo paletó, camisa branca e gravata dos personagens originais.
    pygame.draw.line(tela, terno, (x + 10, y + 34), (x + 4, y + 62), 8)
    pygame.draw.line(tela, terno, (x + 32, y + 34), (x + 38, y + 62), 8)
    pygame.draw.circle(tela, pele, (x + 4, y + 65), 4)
    pygame.draw.circle(tela, pele, (x + 38, y + 65), 4)
    pygame.draw.rect(tela, terno, (x + 9, y + 30, 25, 38), border_radius=5)
    pygame.draw.polygon(tela, BRANCO,
                        [(x + 15, y + 31), (x + 28, y + 31), (x + 21, y + 56)])
    pygame.draw.polygon(tela, gravata,
                        [(x + 21, y + 34), (x + 25, y + 46),
                         (x + 21, y + 52), (x + 18, y + 46)])
    pygame.draw.line(tela, (101, 113, 135), (x + 12, y + 34), (x + 21, y + 58), 2)
    pygame.draw.line(tela, (101, 113, 135), (x + 30, y + 34), (x + 21, y + 58), 2)
    pygame.draw.circle(tela, BRANCO, (x + 22, y + 61), 1)

    if numero <= limite:
        # Raposa humanizada: orelhas pontudas, focinho claro e nariz preto.
        pygame.draw.polygon(tela, pele, [(x + 9, y + 13), (x + 8, y - 3),
                                        (x + 19, y + 7)])
        pygame.draw.polygon(tela, pele, [(x + 26, y + 7), (x + 36, y - 3),
                                        (x + 34, y + 15)])
        pygame.draw.polygon(tela, (242, 177, 153),
                            [(x + 11, y + 8), (x + 10, y + 1), (x + 16, y + 8)])
        pygame.draw.polygon(tela, (242, 177, 153),
                            [(x + 29, y + 8), (x + 34, y + 1), (x + 33, y + 9)])
        pygame.draw.ellipse(tela, pele, (x + 8, y + 5, 28, 26))
        pygame.draw.polygon(tela, (247, 226, 199),
                            [(x + 13, y + 21), (x + 23, y + 30), (x + 33, y + 21)])
        pygame.draw.circle(tela, TEXTO, (x + 18, y + 17), 2)
        pygame.draw.circle(tela, TEXTO, (x + 29, y + 17), 2)
        pygame.draw.circle(tela, TEXTO, (x + 23, y + 25), 3)
    else:
        # Jacaré humanizado: crista, focinho comprido e dentes claros.
        pygame.draw.polygon(tela, (44, 101, 58),
                            [(x + 9, y + 11), (x + 11, y + 1), (x + 17, y + 9),
                             (x + 22, y + 1), (x + 28, y + 9), (x + 34, y + 5),
                             (x + 34, y + 16)])
        pygame.draw.ellipse(tela, pele, (x + 8, y + 7, 28, 24))
        pygame.draw.ellipse(tela, pele, (x + 16, y + 20, 29, 13))
        pygame.draw.line(tela, (35, 76, 48), (x + 20, y + 28), (x + 42, y + 28), 2)
        pygame.draw.polygon(tela, BRANCO,
                            [(x + 26, y + 28), (x + 29, y + 33), (x + 32, y + 28)])
        pygame.draw.polygon(tela, BRANCO,
                            [(x + 35, y + 28), (x + 38, y + 32), (x + 40, y + 28)])
        pygame.draw.circle(tela, TEXTO, (x + 18, y + 17), 2)
        pygame.draw.circle(tela, TEXTO, (x + 29, y + 17), 2)
        pygame.draw.circle(tela, (34, 83, 49), (x + 40, y + 24), 2)

    # Mantém os óculos de dois personagens da versão original.
    if numero == 2 or numero == 5:
        pygame.draw.circle(tela, TEXTO, (x + 18, y + 17), 5, 1)
        pygame.draw.circle(tela, TEXTO, (x + 29, y + 17), 5, 1)

def desenhar_alunos(tela, margem, x_inicial, y_inicial, selecionados, fase):
    """Coloca até seis alunos em fila na margem e devolve suas áreas de clique."""
    areas = []
    fonte_nome = pygame.font.Font(None, 18)

    espacamento = 48 if fase == 1 else 36

    for indice in range(len(margem)):
        numero = margem[indice]
        # Na fase 2 o espaçamento diminui para caberem oito personagens.
        x = x_inicial + indice * espacamento
        y = y_inicial
        area = (x, y, 46, 120)

        if numero in selecionados:
            # O aluno selecionado aparece no barco. O círculo permite retirá-lo.
            pygame.draw.ellipse(tela, (243, 193, 78), (x, y + 78, 43, 16), 3)
            desenhar_texto(tela, "a bordo", fonte_nome, TEXTO, x + 23, y + 65, True)
        else:
            desenhar_personagem(tela, numero, x, y, fase)

        desenhar_texto(tela, nome_personagem(numero, fase), fonte_nome, TEXTO,
                       x + 23, y + 108, True)
        areas.append((numero, area))

    return areas

def desenhar_jogo(tela, fonte_titulo, fonte, esquerda, direita, barco,
                  selecionados, jogadas, estado, mensagem, mouse, fase, progresso=1, angulo=0):
    """Desenha o cenário de lado: chão, rio, alunos em pé e barco."""
    # Céu em degradê para dar profundidade sem depender de outra imagem.
    topo = (74, 126, 160) if fase == 1 else (92, 101, 135)
    base = (190, 215, 211) if fase == 1 else (224, 164, 125)
    for y in range(0, 440):
        parte = y / 440
        cor = (
            int(topo[0] + (base[0] - topo[0]) * parte),
            int(topo[1] + (base[1] - topo[1]) * parte),
            int(topo[2] + (base[2] - topo[2]) * parte)
        )
        pygame.draw.line(tela, cor, (0, y), (1000, y))

    # Sol discreto e nuvens formadas por círculos irregulares.
    pygame.draw.circle(tela, (246, 210, 145), (845, 145), 31)
    for cx, cy, escala in [(135, 150, 1.0), (470, 125, 0.8), (720, 190, 0.65)]:
        cor_nuvem = (236, 239, 233)
        pygame.draw.circle(tela, cor_nuvem, (cx, cy), int(25 * escala))
        pygame.draw.circle(tela, cor_nuvem, (cx + int(27*escala), cy - int(9*escala)), int(31*escala))
        pygame.draw.circle(tela, cor_nuvem, (cx + int(57*escala), cy), int(23*escala))
        pygame.draw.ellipse(tela, cor_nuvem, (cx-int(10*escala), cy, int(90*escala), int(30*escala)))

    # Montanhas em camadas, com silhuetas menos geométricas.
    pygame.draw.polygon(tela, (123, 153, 145),
        [(0,360),(0,325),(75,285),(135,315),(205,250),(280,315),(350,280),(430,350),(430,440),(0,440)])
    pygame.draw.polygon(tela, (101, 137, 124),
        [(570,440),(570,350),(635,305),(700,330),(770,260),(835,315),(900,275),(1000,335),(1000,440)])
    pygame.draw.polygon(tela, (84, 124, 103),
        [(0,440),(0,385),(85,370),(150,395),(230,350),(310,390),(390,365),(470,420),(560,385),(650,410),(730,365),(820,405),(910,370),(1000,395),(1000,440)])

    # Rio e margens com contornos irregulares.
    pygame.draw.rect(tela, (65, 135, 164), (300, 438, 400, 70))
    pygame.draw.polygon(tela, (132, 103, 72), [(0,430),(300,430),(315,452),(300,505),(0,505)])
    pygame.draw.polygon(tela, (132, 103, 72), [(700,430),(1000,430),(1000,505),(700,505),(685,455)])
    pygame.draw.polygon(tela, (79, 132, 86), [(0,425),(70,420),(145,427),(220,417),(300,426),(305,442),(0,442)])
    pygame.draw.polygon(tela, (79, 132, 86), [(695,442),(700,426),(770,418),(845,427),(920,417),(1000,424),(1000,442)])

    # Pequenos reflexos deixam a água menos chapada.
    for x, y, largura_onda in [(320,458,45),(390,482,62),(485,462,38),(545,490,70),(625,470,42)]:
        pygame.draw.arc(tela, (155, 205, 215), (x, y, largura_onda, 12), 0.2, 2.9, 2)

    desenhar_texto(tela, "MARGEM A", fonte, TEXTO, 150, 300, True)
    desenhar_texto(tela, "MARGEM B", fonte, TEXTO, 845, 300, True)
    areas_esquerda = desenhar_alunos(tela, esquerda, 8, 342, selecionados, fase)
    areas_direita = desenhar_alunos(tela, direita, 702, 342, selecionados, fase)

    # Desenha a canoa em uma superfície separada para poder movê-la e virá-la.
    x_destino = 315 if barco == 0 else 525
    if estado == "animando":
        x_origem = 525 if barco == 0 else 315
        x_barco = x_origem + (x_destino - x_origem) * progresso
    else:
        x_barco = x_destino

    canoa = pygame.Surface((160, 125), pygame.SRCALPHA)
    for indice in range(len(selecionados)):
        numero = selecionados[indice]
        desenhar_personagem(canoa, numero, 12 + indice * 45, 5, fase)

    pygame.draw.polygon(canoa, (121, 76, 44),
                        [(0, 88), (150, 88), (130, 120), (22, 120)])
    pygame.draw.line(canoa, (228, 177, 109), (0, 88), (150, 88), 5)
    desenhar_texto(canoa, "LinkedIn Express", pygame.font.Font(None, 19),
                   BRANCO, 75, 105, True)

    canoa = pygame.transform.rotate(canoa, angulo)
    area_canoa = canoa.get_rect(center=(int(x_barco) + 80, 405))
    tela.blit(canoa, area_canoa)

    # Os resultados usam a própria tela do jogo: continuam sendo três telas.
    pygame.draw.rect(tela, (232, 229, 217), (0, 505, 1000, 195))
    desenhar_texto(tela, "Travessias: " + str(jogadas), fonte, TEXTO, 500, 525, True)
    if estado in ("jogando", "animando", "virando"):
        aviso = "Clique nos alunos para embarcar. Clique no lugar deles para retirar."
        if mensagem != "":
            aviso = mensagem
        desenhar_texto(tela, aviso, pygame.font.Font(None, 25), TEXTO, 500, 565, True)
        if estado != "jogando":
            aviso = "A canoa está atravessando..." if estado == "animando" else "A canoa virou!"
            desenhar_texto(tela, aviso, pygame.font.Font(None, 25), VERMELHO, 500, 585, True)
        desenhar_botao(tela, "Menu", (35, 600, 145, 55), fonte, mouse)
        desenhar_botao(tela, "Atravessar", (405, 600, 190, 55), fonte, mouse)
        desenhar_botao(tela, "Reiniciar", (820, 600, 145, 55), fonte, mouse)
    else:
        if estado == "vitoria":
            titulo = "Vitória!"
        else:
            titulo = "A canoa virou! Todos morreram."
        desenhar_texto(tela, titulo, fonte, TEXTO, 500, 555, True)
        desenhar_texto(tela, mensagem, pygame.font.Font(None, 24), TEXTO, 500, 582, True)
        desenhar_botao(tela, "Jogar novamente", (330, 620, 210, 52), fonte, mouse)
        desenhar_botao(tela, "Menu", (565, 620, 145, 52), fonte, mouse)

    return areas_esquerda, areas_direita