"""Movimento adaptado do exemplo car.py fornecido para a prática."""

import random

import pygame


def mover_personagem(posicao, retangulo, direcao, velocidade, dt, area):
    vetor = pygame.Vector2(direcao)
    if vetor.length_squared():
        posicao += vetor.normalize() * velocidade * dt
    posicao.x = max(area.left, min(posicao.x, area.right - retangulo.width))
    posicao.y = max(area.top, min(posicao.y, area.bottom - retangulo.height))
    retangulo.topleft = (round(posicao.x), round(posicao.y))


class Obstaculo:
    """Bloco que desce e reaparece no topo, como no exemplo do carrinho."""

    def __init__(self, area):
        self.area = area.copy()
        self.rect = pygame.Rect(0, 0, 90, 24)
        self.velocidade = 180
        self.reiniciar()

    def reiniciar(self):
        self.rect.x = random.randint(self.area.left, self.area.right - self.rect.width)
        self.rect.bottom = self.area.top
        self.y = float(self.rect.y)

    def atualizar(self, dt):
        self.y += self.velocidade * dt
        self.rect.y = round(self.y)
        if self.rect.top >= self.area.bottom:
            self.reiniciar()
