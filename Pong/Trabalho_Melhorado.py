from random import choice, random
import turtle
from freegames import vector
import os

ARQUIVO_PONTOS = "pontuacoes.txt"
ARQUIVO_CONTADOR = "contador.txt"


nome_jogador1 = turtle.textinput("Pong", "Digite o nome do Jogador 1:")
nome_jogador2 = turtle.textinput("Pong", "Digite o nome do Jogador 2:")


# como forma de melhorar o código, além de implementar a separação do histórico por numero do jogo e quem jogou ele, coloquei tmb a rodada a qual o ponto foi feito pelo jogador, a opção de apagar o historico pelo terminal sempre que for mostrado o historico de jogos, mas também um layout mais bonitinho nos arquivos txt, falar que a parte do contador pode parecer simples, mas teve todo um caminho, mas bem, agora o código está bem mais completo.

def carregar_contador():
    if os.path.exists(ARQUIVO_CONTADOR):
        with open(ARQUIVO_CONTADOR, "r") as f:
            return int(f.read())
    return 0
contador = carregar_contador()
def salvar_contador(valor):
    with open(ARQUIVO_CONTADOR, "w") as f:
        f.write(str(valor))

def iniciar_novo_jogo():
    global contador
    contador += 1
    salvar_contador(contador)

    with open(ARQUIVO_PONTOS, "a", encoding="utf-8") as f:
        f.write(f"\n\nJOGO Nº {contador}\n")
        f.write("==" * 20)
        f.write(f"\n{nome_jogador1} vs {nome_jogador2}\n")
        f.write("==" * 20)

def salvar_resultado(jogador, pontos):
    with open(ARQUIVO_PONTOS, "a", encoding="utf-8") as f:
        f.write(f"\n{jogador}: {pontos} ° ponto na rodada {rodada}\n")

def listar_resultados():
    print("\n=== HISTÓRICO DE JOGOS ===")
    try:
        with open(ARQUIVO_PONTOS, "r", encoding="utf-8") as f:
            print(f.read())
        perguntar_apagar_historico()
    except FileNotFoundError:
        print("Nenhum jogo registrado ainda.")

def perguntar_apagar_historico():
    resposta = input("\nDeseja apagar o histórico de jogos? (s/n): ").strip().lower()

    if resposta == "s":
        apagar_historico()
    else:
        print("Histórico mantido.")

def apagar_historico():
    if os.path.exists(ARQUIVO_PONTOS):
        open(ARQUIVO_PONTOS, "w").close()
        open(ARQUIVO_CONTADOR, "w").close()
        print("Histórico apagado!")
    else:
        print("Nenhum histórico para apagar.")

def valor():
    return (3 + random() * 2) * choice([1, -1])

def reiniciar_bola(bola, direcao):
    bola.x = 0
    bola.y = 0
    direcao.x = valor()
    direcao.y = valor()

bola = vector(0, 0)
bola2 = vector(20, 30)

direcao = vector(valor(), valor())
direcao2 = vector(valor(), valor())

raquetes = {1: 0, 2: 0}
jogadores = {1: nome_jogador1, 2: nome_jogador2}
pontos = {1: 0, 2: 0}
rodada = 0

PONTOS_PARA_VENCER = 5
jogo_encerrado = False

def mover(jogador, deslocamento):
    raquetes[jogador] += deslocamento

def raquete(x, y, largura, altura, cor):
    turtle.penup()
    turtle.goto(x, y)
    turtle.down()
    turtle.begin_fill()
    turtle.color(cor)
    for _ in range(2):
        turtle.forward(largura)
        turtle.left(90)
        turtle.forward(altura)
        turtle.left(90)
    turtle.end_fill()

def fim_de_jogo(vencedor):
    global jogo_encerrado
    jogo_encerrado = True
    turtle.clear()
    turtle.goto(0, 0)
    turtle.color("white")
    turtle.write(
        f"FIM DE JOGO!\nVencedor: {vencedor}",
        align="center",
        font=("Arial", 18, "bold")
    )
    listar_resultados()

def desenhar():
    if jogo_encerrado:
        return

    turtle.clear()

    raquete(-200, raquetes[1], 10, 100, "blue")
    raquete(180, raquetes[2], 10, 100, "red")

    bola.move(direcao)
    bola2.move(direcao2)

    turtle.up()
    turtle.goto(bola.x, bola.y)
    turtle.dot(10)

    turtle.goto(bola2.x, bola2.y)
    turtle.dot(10)
    global rodada
    if bola.y < -200 or bola.y > 200:
        direcao.y = -direcao.y

    if bola2.y < -200 or bola2.y > 200:
        direcao2.y = -direcao2.y

    if bola.x < -185:
        if raquetes[1] <= bola.y <= raquetes[1] + 100:
            direcao.x = -direcao.x
        else:
            pontos[2] += 1
            rodada +=1
            salvar_resultado(jogadores[2], pontos[2])
            reiniciar_bola(bola, direcao)

    if bola.x > 185:
        if raquetes[2] <= bola.y <= raquetes[2] + 100:
            direcao.x = -direcao.x
        else:
            pontos[1] += 1
            rodada +=1
            salvar_resultado(jogadores[1], pontos[1])
            reiniciar_bola(bola, direcao)
            
    if bola2.x < -185:
        if raquetes[1] <= bola2.y <= raquetes[1] + 100:
            direcao2.x = -direcao2.x
        else:
            pontos[2] += 1
            rodada +=1
            salvar_resultado(jogadores[2], pontos[2])
            reiniciar_bola(bola2, direcao2)
    if bola2.x > 185:
        if raquetes[2] <= bola2.y <= raquetes[2] + 100:
            direcao2.x = -direcao2.x
        else:
            pontos[1] += 1
            rodada +=1
            salvar_resultado(jogadores[1], pontos[1])
            reiniciar_bola(bola2, direcao2)

    global contador
    if pontos[1] >= PONTOS_PARA_VENCER:
        fim_de_jogo(nome_jogador1)
        contador +=1
        return

    if pontos[2] >= PONTOS_PARA_VENCER:
        fim_de_jogo(nome_jogador2)
        contador +=1
        return

    turtle.update()
    turtle.ontimer(desenhar, 40)

turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
turtle.bgcolor("black")

turtle.listen()
turtle.onkey(lambda: mover(1, 20), 'w')
turtle.onkey(lambda: mover(1, -20), 's')
turtle.onkey(lambda: mover(2, 20), 'i')
turtle.onkey(lambda: mover(2, -20), 'k')

iniciar_novo_jogo()
desenhar()
turtle.mainloop()
