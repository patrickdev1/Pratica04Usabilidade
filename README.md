# Rato & Queijo 🐭🧀

Jogo da Prática 04 de Usabilidade, Desenvolvimento Web, Mobile e Jogos, feito em Python com Pygame. Guie o rato até o queijo: cada colisão soma um ponto e faz o queijo reaparecer em outro lugar aleatório.

## Executar no Windows

Instale Python 3.10 ou superior. Dentro da pasta do projeto, execute no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Não é necessário ativar o ambiente virtual. Se o comando `python` não estiver disponível, tente `py` no primeiro comando.

## Controles

| Tecla | Ação |
| --- | --- |
| Setas | Mover o rato |
| Espaço | Pausar ou continuar |
| R | Reiniciar e zerar os pontos |
| Esc | Sair |

O rato fica dentro do campo. O queijo sempre surge inteiramente no campo e fora do rato. Ao trocar de janela, o jogo pausa automaticamente. Não há limite de tempo nem condição de derrota.

## Organização e conceitos

- `main.py`: estado do jogo (`Jogo`), desenhos (`Tela`) e loop principal (`main`).
- `assets/`: sprites incluídos; o jogo funciona sem internet após a instalação.
- `requirements.txt`: dependência do projeto.
- `test_jogo.py`: testes de movimento, colisão, limites, pausa e reinício.

O loop trata eventos, atualiza posições e desenha a tela a 60 FPS. O movimento usa `pygame.key.get_pressed`, `Vector2` e tempo entre quadros. A coleta usa `Rect.colliderect`; o reposicionamento usa `random.randint`.

O requisito corresponde à atividade da página 40 do material `Encontro_06_Jogos_02_Pygame_UDWMJ.pdf`. Os arquivos `car.py` e `colision.py` mencionados no material não vieram anexados; esta implementação é independente, utilizando os conceitos apresentados na aula.

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Créditos dos sprites

Imagens do projeto [Twemoji](https://github.com/twitter/twemoji), copyright Twitter, Inc. e colaboradores, sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). A licença completa está em `assets/LICENSE-GRAPHICS`.

- [Rato, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f401.png)
- [Queijo, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f9c0.png)

Os arquivos originais estão incluídos sem alteração; durante o jogo são redimensionados e o rato pode ser espelhado.
