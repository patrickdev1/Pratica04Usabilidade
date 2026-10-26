"""Colisões com Rect.colliderect, adaptadas do exemplo colision.py."""


def colidiu(primeiro, segundo):
    return primeiro.colliderect(segundo)


class Contato:
    """Conta a entrada em um contato, sem repetir a cada quadro."""

    def __init__(self):
        self.ativo = False

    def atualizar(self, primeiro, segundo):
        anterior = self.ativo
        self.ativo = colidiu(primeiro, segundo)
        return self.ativo and not anterior
