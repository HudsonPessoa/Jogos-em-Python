import random

opcoes = ["pedra", "papel", "tesoura"]
jogador = input("Digite pedra, papel ou tesoura:")
computador = random.choice(opcoes)


print(f"Você escohlheu: {jogador}")
print(f"O computador escohlheu: {computador}")

if jogador == computador:
    print("Empate!")

elif (jogador == "pedra" and computador == "tesoura") or \
     (jogador == "papel" and computador == "pedra") or \
     (jogador == "tesoura" and computador == "papel"):
     print("Você venceu!!!")
else:
     print("Você perdeu!!")