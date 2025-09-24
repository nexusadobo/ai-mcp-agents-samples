class StudentManager:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.grades = []

    def add_grade(self, grade):
        """Add a grade to the student's grade list."""
        self.grades.append(grade)

    def calculate_average(self):
        """Calculate and return the average of the grades."""
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

# Example usage:
# student = StudentManager('John Doe', 20)
# student.add_grade(88)
# student.add_grade(92)
# print(student.calculate_average())
