import os
import random
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

LARGURA, ALTURA = 960, 680
AREA = pygame.Rect(72, 172, 816, 400)
TAMANHO_RATO = 64
TAMANHO_QUEIJO = 48
VELOCIDADE = 280  # pixels por segundo
ASSETS = Path(__file__).resolve().parent / "assets"
CREME = (245, 224, 181)
ESCURO = (49, 36, 34)
AMARELO = (255, 192, 67)


class Jogo:
    def __init__(self):
        self.rato = pygame.Rect(0, 0, TAMANHO_RATO, TAMANHO_RATO)
        self.queijo = pygame.Rect(0, 0, TAMANHO_QUEIJO, TAMANHO_QUEIJO)
        self.reiniciar()

    def reiniciar(self):
        self.rato.center = AREA.center
        self.posicao = pygame.Vector2(self.rato.topleft)
        self.pontos = 0
        self.pausado = False
        self.olhando_direita = False
        self.aviso = 0
        self.sortear_queijo()

    def sortear_queijo(self):
        anterior = self.queijo.copy()
        while True:
            self.queijo.topleft = (
                random.randint(AREA.left, AREA.right - self.queijo.width),
                random.randint(AREA.top, AREA.bottom - self.queijo.height),
            )
            if (not self.queijo.colliderect(self.rato.inflate(24, 24))
                    and not self.queijo.colliderect(anterior)):
                break

    def atualizar(self, direcao, dt):
        if self.pausado:
            return
        self.aviso = max(0, self.aviso - dt)
        vetor = pygame.Vector2(direcao)
        if vetor.length_squared():
            # Mantém a mesma velocidade na diagonal.
            self.posicao += vetor.normalize() * VELOCIDADE * dt
            if vetor.x:
                self.olhando_direita = vetor.x > 0
        self.posicao.x = max(AREA.left, min(self.posicao.x, AREA.right - self.rato.width))
        self.posicao.y = max(AREA.top, min(self.posicao.y, AREA.bottom - self.rato.height))
        self.rato.topleft = (round(self.posicao.x), round(self.posicao.y))
        if self.rato.colliderect(self.queijo):
            self.pontos += 1
            self.aviso = 0.8
            self.sortear_queijo()


class Tela:
    def __init__(self, superficie):
        self.superficie = superficie
        self.titulo = pygame.font.SysFont("consolas", 36, bold=True)
        self.normal = pygame.font.SysFont("consolas", 22, bold=True)
        self.pequena = pygame.font.SysFont("consolas", 16)
        self.rato = pygame.transform.smoothscale(
            pygame.image.load(str(ASSETS / "rato.png")).convert_alpha(), (64, 64))
        self.rato_direita = pygame.transform.flip(self.rato, True, False)
        self.queijo = pygame.transform.smoothscale(
            pygame.image.load(str(ASSETS / "queijo.png")).convert_alpha(), (48, 48))
        self.cenario = self.criar_cozinha()
        self.ultimo_ponto = 0
        self.coleta = (0, 0)

    def criar_cozinha(self):
        # O cenário é desenhado pequeno e ampliado para manter os pixels.
        fundo = pygame.Surface((480, 340))
        fundo.fill(ESCURO)
        madeira = (143, 78, 49)
        luz_madeira = (181, 110, 64)
        rejunte = (160, 151, 128)
        pygame.draw.rect(fundo, madeira, (8, 44, 464, 258))
        pygame.draw.rect(fundo, luz_madeira, (8, 44, 464, 3))
        for x in range(16, 470, 56):
            pygame.draw.line(fundo, (105, 57, 41), (x, 48), (x, 81), 2)
            pygame.draw.rect(fundo, ESCURO, (x + 18, 68, 15, 3))
            pygame.draw.rect(fundo, (218, 158, 89), (x + 18, 67, 15, 1))
        pygame.draw.rect(fundo, (84, 51, 38), (32, 82, 416, 208))
        campo = pygame.Rect(36, 86, 408, 200)
        fundo.set_clip(campo)
        for linha, y in enumerate(range(86, 286, 24)):
            for coluna, x in enumerate(range(36, 444, 24)):
                cor = (226, 214, 180) if (linha + coluna) % 2 == 0 else (151, 171, 157)
                pygame.draw.rect(fundo, rejunte, (x, y, 24, 24))
                pygame.draw.rect(fundo, cor, (x + 1, y + 1, 23, 23))
                if (linha * 7 + coluna * 3) % 13 == 0:
                    pygame.draw.line(fundo, rejunte, (x + 4, y + 19), (x + 9, y + 19))
        fundo.set_clip(None)
        # Fogão, pia e tábua ficam fora da área de movimento.
        pygame.draw.rect(fundo, ESCURO, (24, 48, 62, 29))
        pygame.draw.rect(fundo, (203, 194, 168), (26, 49, 58, 25))
        for x in (40, 69):
            for y in (55, 67):
                pygame.draw.circle(fundo, ESCURO, (x, y), 5)
                pygame.draw.circle(fundo, (112, 108, 99), (x, y), 2)
        pygame.draw.rect(fundo, (200, 193, 169), (371, 48, 69, 28))
        pygame.draw.rect(fundo, (94, 123, 124), (376, 52, 58, 20))
        pygame.draw.rect(fundo, (143, 172, 164), (379, 54, 52, 15))
        pygame.draw.circle(fundo, ESCURO, (406, 63), 2)
        pygame.draw.lines(fundo, ESCURO, False, [(402, 49), (402, 44), (409, 44), (409, 53)], 3)
        pygame.draw.lines(fundo, (220, 218, 191), False, [(402, 48), (402, 44), (408, 44), (408, 52)], 1)
        pygame.draw.rect(fundo, (230, 176, 104), (215, 49, 57, 26))
        pygame.draw.rect(fundo, (188, 129, 74), (219, 52, 49, 20), 1)
        pygame.draw.line(fundo, (245, 213, 151), (223, 55), (255, 55))
        pygame.draw.polygon(fundo, (219, 220, 198), [(242, 59), (262, 59), (257, 63), (242, 63)])
        pygame.draw.rect(fundo, ESCURO, (231, 59, 11, 4))
        for x in (15, 451):
            for y in (94, 154, 214):
                pygame.draw.rect(fundo, (111, 62, 44), (x, y, 14, 50), 1)
                pygame.draw.rect(fundo, (224, 167, 101), (x + 5, y + 20, 3, 10))
        pygame.draw.ellipse(fundo, ESCURO, (19, 242, 16, 25))
        pygame.draw.rect(fundo, ESCURO, (19, 254, 16, 13))
        pygame.draw.rect(fundo, (79, 47, 37), (8, 290, 464, 12))
        for x in range(14, 466, 28):
            pygame.draw.line(fundo, (155, 96, 58), (x, 293), (x + 19, 293))
        return pygame.transform.scale(fundo, (LARGURA, ALTURA))

    def texto(self, mensagem, fonte, cor, posicao, centro=False):
        imagem = fonte.render(mensagem, False, cor)
        retangulo = imagem.get_rect(center=posicao) if centro else imagem.get_rect(topleft=posicao)
        self.superficie.blit(imagem, retangulo)

    def desenhar(self, jogo):
        tela = self.superficie
        tela.blit(self.cenario, (0, 0))
        self.texto("RATO NA COZINHA", self.titulo, ESCURO, (29, 22))
        self.texto("RATO NA COZINHA", self.titulo, AMARELO, (26, 19))
        self.texto("O jantar ficou por sua conta.", self.pequena, CREME, (28, 60))
        self.texto("QUEIJOS", self.pequena, CREME, (751, 18))
        self.texto(f"{jogo.pontos:03d}", self.titulo, AMARELO, (748, 35))
        tela.blit(self.queijo, (855, 23))
        pygame.draw.ellipse(tela, (125, 132, 112), (jogo.queijo.x + 7, jogo.queijo.y + 34, 35, 10))
        tela.blit(self.queijo, jogo.queijo)
        pygame.draw.ellipse(tela, (125, 132, 112), (jogo.rato.x + 8, jogo.rato.y + 44, 47, 11))
        tela.blit(self.rato_direita if jogo.olhando_direita else self.rato, jogo.rato)
        if jogo.pontos > self.ultimo_ponto:
            self.coleta = jogo.rato.center
        self.ultimo_ponto = jogo.pontos
        if jogo.aviso:
            progresso = 1 - jogo.aviso / 0.8
            x, y = self.coleta
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                distancia = 22 + progresso * 26
                pygame.draw.rect(tela, AMARELO, (int(x + dx * distancia), int(y + dy * distancia), 5, 5))
            self.texto("+1", self.normal, ESCURO,
                       (x, max(AREA.top + 12, y - 30 - progresso * 24)), True)
        for x, tecla, acao in [(28, "SETAS", "mover"), (250, "ESPAÇO", "pausa"),
                               (498, "R", "reiniciar"), (755, "ESC", "sair")]:
            largura = self.pequena.size(tecla)[0] + 18
            pygame.draw.rect(tela, (117, 82, 61), (x + 2, 625, largura, 27))
            pygame.draw.rect(tela, CREME, (x, 622, largura, 27))
            self.texto(tecla, self.pequena, ESCURO, (x + 9, 627))
            self.texto(acao, self.pequena, CREME, (x + largura + 10, 627))
        if jogo.pausado:
            sombra = pygame.Surface(AREA.size, pygame.SRCALPHA)
            sombra.fill((35, 28, 25, 130))
            tela.blit(sombra, AREA)
            pygame.draw.rect(tela, ESCURO, (289, 299, 390, 134))
            pygame.draw.rect(tela, CREME, (280, 290, 390, 134))
            pygame.draw.rect(tela, (143, 78, 49), (287, 297, 376, 120), 2)
            self.texto("PAUSA", self.titulo, ESCURO, (475, 334), True)
            self.texto("ESPAÇO para voltar", self.normal, ESCURO, (475, 381), True)


def main():
    pygame.display.init()
    pygame.font.init()
    try:
        superficie = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Rato na Cozinha")
        tela = Tela(superficie)
        pygame.display.set_icon(tela.queijo)
        jogo = Jogo()
        relogio = pygame.time.Clock()
        executando = True
        while executando:
            dt = min(relogio.tick(60) / 1000, 0.05)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    executando = False
                elif evento.type == pygame.WINDOWFOCUSLOST:
                    jogo.pausado = True
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        executando = False
                    elif evento.key == pygame.K_SPACE:
                        jogo.pausado = not jogo.pausado
                    elif evento.key == pygame.K_r:
                        jogo.reiniciar()
            teclas = pygame.key.get_pressed()
            jogo.atualizar((int(teclas[pygame.K_RIGHT]) - int(teclas[pygame.K_LEFT]),
                            int(teclas[pygame.K_DOWN]) - int(teclas[pygame.K_UP])), dt)
            tela.desenhar(jogo)
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
