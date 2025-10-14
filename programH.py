class Power:
    def pow(self, x, n):
        result = 1
        if n >= 0:
            for i in range(n):
                result *= x
        else:
            for i in range(-n):
                result /= x
        return result

# Example usage
x = float(input("Enter number (x): "))
n = int(input("Enter power (n): "))

p = Power()
print(f"{x} raised to power {n} is:", p.pow(x, n))
