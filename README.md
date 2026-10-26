# Rato na Cozinha

Jogo em Python com Pygame para a Prática 04 de Usabilidade, Desenvolvimento Web, Mobile e Jogos.

O objetivo é mover o rato até o queijo usando as setas do teclado. Quando o rato encosta no queijo, ganha um ponto e o queijo aparece em outra posição aleatória.

Desvie também do bloco verde que atravessa a cozinha de cima para baixo. Ao encostar nele, o bloco fica vermelho, o rato recebe um contorno vermelho e aparece um aviso. O contador registra uma colisão por contato, sem repetir enquanto os retângulos continuam sobrepostos. As colisões não retiram pontos nem encerram a partida.

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
| R | Reiniciar e zerar pontos e colisões |
| Esc | Sair |

O cenário é uma cozinha com piso quadriculado, fogão e pia. Os móveis são só parte do cenário e ficam fora do espaço onde o rato anda. O jogo não tem limite de tempo. Ao trocar de janela, ele pausa automaticamente.

## Arquivos

- `main.py`: código do jogo.
- `car.py`: movimento do rato e do obstáculo, adaptado do exemplo do carrinho.
- `colision.py`: detecção de colisões e controle de início de cada contato, adaptados do exemplo dos dois retângulos.
- `assets/`: imagens do rato e do queijo e licença de uso.
- `requirements.txt`: versão do Pygame usada no projeto.
- `test_jogo.py`: testes das regras do jogo.

## Uso dos exemplos da prática

Os dois arquivos fornecidos foram adaptados como módulos importados pelo jogo. O `car.py` fornece o movimento controlado pelas setas e o bloco que desce e reaparece em uma posição horizontal aleatória. O rato usa a imagem existente, por isso não é necessário ter `car.png`. O movimento usa pixels por segundo e respeita os limites da cozinha.

O `colision.py` usa `Rect.colliderect` tanto para coletar queijo quanto para detectar o obstáculo. Essa função também reconhece quando um retângulo contém completamente o outro. A mudança de cor do exemplo aparece no bloco durante o contato. Execute `main.py` para jogar; os módulos não abrem janelas separadas.

## Testes

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

## Imagens

As imagens são do [Twemoji](https://github.com/twitter/twemoji), de Twitter, Inc. e colaboradores, e usam a licença [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Uma cópia da licença está em `assets/LICENSE-GRAPHICS`.

- [Rato, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f401.png)
- [Queijo, versão 14.0.2](https://raw.githubusercontent.com/twitter/twemoji/v14.0.2/assets/72x72/1f9c0.png)

As imagens são redimensionadas no jogo, e o rato é espelhado quando muda de direção.
