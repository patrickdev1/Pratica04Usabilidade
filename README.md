# Rato e Queijo

Jogo em Python com Pygame para a Prática 04 de Usabilidade, Desenvolvimento Web, Mobile e Jogos.

O objetivo é mover o rato até o queijo usando as setas do teclado. Quando o rato encosta no queijo, ganha um ponto e o queijo aparece em outra posição aleatória.

## Como jogar

Com Python 3.10 ou superior instalado, abra o PowerShell na pasta do projeto e execute:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Se o Windows não reconhecer `python`, use `py` no primeiro comando.

## Controles

| Tecla | Ação |
| --- | --- |
| Setas | Mover o rato |
| Espaço | Pausar ou continuar |
| R | Reiniciar e zerar os pontos |
| Esc | Sair |

O jogo não tem limite de tempo. Ao trocar de janela, ele pausa automaticamente.

## Arquivos

- `main.py`: código do jogo.
- `assets/`: imagens do rato e do queijo e licença de uso.
- `requirements.txt`: versão do Pygame usada no projeto.
- `test_jogo.py`: testes das regras do jogo.


## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Imagens

As imagens são do [Twemoji](https://github.com/twitter/twemoji), de Twitter, Inc. e colaboradores, e usam a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Uma cópia da licença está em `assets/LICENSE-GRAPHICS`.

- [Rato, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f401.png)
- [Queijo, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f9c0.png)

As imagens são redimensionadas no jogo, e o rato é espelhado quando muda de direção.
