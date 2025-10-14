class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14 * self.radius

# Example usage
r = float(input("Enter radius of circle: "))
c = Circle(r)
print("Area of Circle:", c.area())
print("Perimeter of Circle:", c.perimeter())
