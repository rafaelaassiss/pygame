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

