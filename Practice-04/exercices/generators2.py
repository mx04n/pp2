n = int(input())

even_numbers = (str(i) for i in range(n + 1) if (i % 3 == 0 and i % 4 == 0) )

print(",".join(even_numbers))