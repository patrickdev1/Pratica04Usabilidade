import os
import random
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

LARGURA, ALTURA = 960, 680
AREA = pygame.Rect(32, 130, 896, 474)
TAMANHO_RATO = 64
TAMANHO_QUEIJO = 48
VELOCIDADE = 280  # pixels por segundo
ASSETS = Path(__file__).resolve().parent / "assets"
FUNDO = (247, 242, 229)
TEXTO = (47, 61, 49)
VERDE = (53, 93, 65)


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
        self.titulo = pygame.font.SysFont("segoeui", 36, bold=True)
        self.normal = pygame.font.SysFont("segoeui", 20)
        self.pequena = pygame.font.SysFont("segoeui", 16)
        self.rato = pygame.transform.smoothscale(
            pygame.image.load(str(ASSETS / "rato.png")).convert_alpha(), (64, 64))
        self.rato_direita = pygame.transform.flip(self.rato, True, False)
        self.queijo = pygame.transform.smoothscale(
            pygame.image.load(str(ASSETS / "queijo.png")).convert_alpha(), (48, 48))

    def texto(self, mensagem, fonte, cor, posicao, centro=False):
        imagem = fonte.render(mensagem, True, cor)
        retangulo = imagem.get_rect(center=posicao) if centro else imagem.get_rect(topleft=posicao)
        self.superficie.blit(imagem, retangulo)

    def desenhar(self, jogo):
        tela = self.superficie
        tela.fill(FUNDO)
        self.texto("Rato & Queijo", self.titulo, TEXTO, (32, 24))
        self.texto("Use as setas para pegar o queijo.", self.normal, VERDE, (34, 77))
        pygame.draw.rect(tela, VERDE, (738, 30, 190, 66), border_radius=16)
        self.texto(f"Queijos: {jogo.pontos:02d}", self.normal, (255, 255, 255), (833, 63), True)
        pygame.draw.rect(tela, (224, 231, 209), AREA, border_radius=18)
        for x in range(56, AREA.right - 12, 32):
            for y in range(154, AREA.bottom - 12, 32):
                pygame.draw.circle(tela, (202, 214, 186), (x, y), 2)
        pygame.draw.ellipse(tela, (190, 202, 171), jogo.queijo.move(0, 6).inflate(-4, -26))
        tela.blit(self.queijo, jogo.queijo)
        tela.blit(self.rato_direita if jogo.olhando_direita else self.rato, jogo.rato)
        self.texto("SETAS  mover     |     ESPAÇO  pausar     |     R  reiniciar     |     ESC  sair",
                   self.pequena, TEXTO, (480, 635), True)
        if jogo.aviso:
            self.texto("+1 queijo!", self.normal, VERDE, (480, 108), True)
        if jogo.pausado:
            sombra = pygame.Surface(AREA.size, pygame.SRCALPHA)
            sombra.fill((35, 48, 36, 170))
            tela.blit(sombra, AREA)
            self.texto("Jogo pausado", self.titulo, FUNDO, (480, 335), True)
            self.texto("Pressione ESPAÇO para continuar", self.normal, FUNDO, (480, 385), True)


def main():
    pygame.display.init()
    pygame.font.init()
    try:
        superficie = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Rato & Queijo | Prática 04")
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
