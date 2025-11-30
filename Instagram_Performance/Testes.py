import random

lista = []

numeros = [random.randint(1, 100) for _ in range(10)]
lista.append(numeros)

print("\n===NÚMEROS SORTEADOS====\n")

for i in range(10):
    print(f"Número {i + 1}: {lista[0][i]}")

print("\n===NÚMEROS PARES===\n")
pares = [num for num in lista[0] if num % 2 == 0]
for par in pares:
    print(f"Número par: {par}")