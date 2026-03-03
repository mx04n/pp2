N = int(input())

squares = (i ** 2 for i in range(1, N + 1))

for square in squares:
    print(square)