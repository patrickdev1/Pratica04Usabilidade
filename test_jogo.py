import unittest

import pygame
from main import AREA, Jogo, VELOCIDADE


class TestJogo(unittest.TestCase):
    def test_colisao_conta_apenas_entrada_inclusive_contencao(self):
        jogo = Jogo()
        jogo.obstaculo.rect = jogo.rato.inflate(20, 20)
        jogo.obstaculo.y = float(jogo.obstaculo.rect.y)
        jogo.atualizar((0, 0), 0)
        jogo.atualizar((0, 0), 0)
        self.assertEqual(jogo.colisoes, 1)
        self.assertTrue(jogo.contato.ativo)
        self.assertGreater(jogo.aviso_colisao, 0)
        jogo.obstaculo.reiniciar()
        jogo.atualizar((0, 0), 0)
        self.assertFalse(jogo.contato.ativo)
        jogo.obstaculo.rect.center = jogo.rato.center
        jogo.obstaculo.y = float(jogo.obstaculo.rect.y)
        jogo.atualizar((0, 0), 0)
        self.assertEqual(jogo.colisoes, 2)

    def test_obstaculo_move_reaparece_e_pausa(self):
        jogo = Jogo()
        bloco = jogo.obstaculo
        inicio = bloco.y
        jogo.atualizar((0, 0), 0.1)
        self.assertAlmostEqual(bloco.y - inicio, bloco.velocidade * 0.1)
        jogo.pausado = True
        anterior = bloco.rect.copy()
        jogo.atualizar((0, 0), 1)
        self.assertEqual(bloco.rect, anterior)
        jogo.pausado = False
        bloco.y = float(AREA.bottom)
        jogo.atualizar((0, 0), 0)
        self.assertEqual(bloco.rect.bottom, AREA.top)
        self.assertGreaterEqual(bloco.rect.left, AREA.left)
        self.assertLessEqual(bloco.rect.right, AREA.right)
        jogo.colisoes = 5
        jogo.reiniciar()
        self.assertEqual(jogo.colisoes, 0)
        self.assertFalse(jogo.contato.ativo)
        self.assertEqual(jogo.aviso_colisao, 0)

    def test_queijo_dentro_do_campo_e_fora_do_rato(self):
        jogo = Jogo()
        for _ in range(500):
            anterior = jogo.queijo.copy()
            jogo.sortear_queijo()
            self.assertTrue(AREA.contains(jogo.queijo))
            self.assertFalse(jogo.queijo.colliderect(jogo.rato))
            self.assertFalse(jogo.queijo.colliderect(anterior))

    def test_coleta_soma_uma_vez_e_reposiciona(self):
        jogo = Jogo()
        jogo.queijo.center = jogo.rato.center
        anterior = jogo.queijo.copy()
        jogo.atualizar((0, 0), 0)
        self.assertEqual(jogo.pontos, 1)
        self.assertFalse(jogo.queijo.colliderect(anterior))
        jogo.atualizar((0, 0), 0)
        self.assertEqual(jogo.pontos, 1)

    def test_limites_em_todas_as_direcoes(self):
        jogo = Jogo()
        for direcao in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            jogo.atualizar(direcao, 10)
            self.assertTrue(AREA.contains(jogo.rato))

    def test_velocidade_diagonal_e_constante(self):
        jogo = Jogo()
        origem = jogo.posicao.copy()
        jogo.atualizar((1, 1), 0.1)
        self.assertAlmostEqual(jogo.posicao.distance_to(origem), VELOCIDADE * 0.1)

    def test_pausa_e_reinicio(self):
        jogo = Jogo()
        origem = jogo.rato.copy()
        jogo.pausado = True
        jogo.atualizar((1, 0), 1)
        self.assertEqual(jogo.rato, origem)
        jogo.pontos = 8
        jogo.reiniciar()
        self.assertEqual(jogo.pontos, 0)
        self.assertFalse(jogo.pausado)
        self.assertEqual(jogo.rato.center, AREA.center)


if __name__ == "__main__":
    unittest.main()
