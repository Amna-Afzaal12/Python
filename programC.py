def even_numbers(n):
    evens = []
    for i in range(2, 2 * n + 1, 2):
        print(i, end=" ")
        evens.append(i)
    return evens

n = int(input("Enter how many even numbers: "))
numbers = even_numbers(n)

sum_even = sum(numbers)
product_even = 1
for num in numbers:
    product_even *= num

print("\nSum of even numbers:", sum_even)
print("Product of even numbers:", product_even)
