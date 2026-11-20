import io
import random  # Permite sortear uma frase da lista com random.choice().
import math
import struct
import wave
import pygame
import csv
from pathlib import Path

# ---------------- ETAPA 2: DADOS GERAIS DO JOGO ----------------
LARGURA = 1000
ALTURA = 700
NOMES_FASE1 = ["Insper 1", "Insper 2", "Insper 3", "FGV 1", "FGV 2", "FGV 3"]
NOMES_FASE2 = ["Insper 1", "Insper 2", "Insper 3", "Insper 4",
               "FGV 1", "FGV 2", "FGV 3", "FGV 4"]

def nome_personagem(numero, fase):
    if fase == 1:
        return NOMES_FASE1[numero - 1]
    return NOMES_FASE2[numero - 1]

# Cada texto entre aspas é um elemento da lista de falas.
# O sorteio acontece ao embarcar, e não a cada quadro da tela.
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
  














