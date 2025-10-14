class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Job:
    def __init__(self, designation, salary):
        self.designation = designation
        self.salary = salary

class Employee(Person, Job):
    def __init__(self, name, age, designation, salary):
        Person.__init__(self, name, age)
        Job.__init__(self, designation, salary)

    def display_details(self):
        print("Employee Name:", self.name)
        print("Age:", self.age)
        print("Designation:", self.designation)
        print("Salary:", self.salary)

# Example usage
emp = Employee("John", 32, "Software Engineer", 50000)
emp.display_details()
