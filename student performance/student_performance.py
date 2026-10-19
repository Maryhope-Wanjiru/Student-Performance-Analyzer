import csv
from abc import ABC, abstractmethod


# Task 2: Base class (encapsulation + abstraction)
class Student(ABC):

    def __init__(self, student_id, first_name, last_name, programme, marks):
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme
        self._marks = dict(marks)

    @property
    def student_id(self):
        return self._student_id

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    @property
    def programme(self):
        return self._programme

    @property
    def marks(self):
        return dict(self._marks)

    def update_mark(self, subject, new_mark):
        if subject not in self._marks:
            raise KeyError(f"Unknown subject: {subject}")
        if not isinstance(new_mark, (int, float)) or not 0 <= new_mark <= 100:
            raise ValueError("Mark must be a number between 0 and 100")
        self._marks[subject] = new_mark

    # Task 6: flexible interface using variable-length arguments
    @staticmethod
    def calculate_average(*marks):
        if len(marks) == 0:
            raise ValueError("At least one mark is required")
        for m in marks:
            if not isinstance(m, (int, float)) or isinstance(m, bool):
                raise TypeError(f"Marks must be numbers, got: {m!r}")
            if not 0 <= m <= 100:
                raise ValueError(f"Mark out of range (0-100): {m}")
        return sum(marks) / len(marks)

    def average(self):
        return self.calculate_average(*self._marks.values())

    def grade(self):
        avg = self.average()
        if avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        elif avg >= 50:
            return "D"
        return "F"

    @abstractmethod
    def get_status(self):
        pass

    # Task 7: report for one student
    def generate_report(self):
        lines = [
            f"Student ID : {self.student_id}",
            f"Name       : {self.full_name}",
            f"Programme  : {self.programme}",
            "Marks      : " + ", ".join(f"{s}: {m}" for s, m in self._marks.items()),
            f"Average    : {self.average():.2f}",
            f"Grade      : {self.grade()}",
            f"Status     : {self.get_status()}",
        ]
        return "\n".join(lines)


class AIUStudent(Student):

    def get_status(self):
        return "Regular student"


# Task 4: Inheritance and method overriding
class ScholarshipStudent(AIUStudent):

    ELIGIBILITY_THRESHOLD = 85

    def __init__(self, student_id, first_name, last_name, programme, marks,
                 scholarship_amount=0):
        super().__init__(student_id, first_name, last_name, programme, marks)
        self.scholarship_amount = scholarship_amount

    def is_eligible(self):
        return self.average() >= self.ELIGIBILITY_THRESHOLD

    def get_status(self):
        if self.is_eligible():
            return f"Scholarship ELIGIBLE (Amount: {self.scholarship_amount:,})"
        return "Scholarship student - NOT eligible (average below 85)"

    def generate_report(self):
        base = super().generate_report()
        eligibility = "Yes" if self.is_eligible() else "No"
        return base + f"\nScholarship Eligible : {eligibility}"


# Task 3: PerformanceAnalyzer
class PerformanceAnalyzer:

    def __init__(self, students):
        self._students = list(students)

    def highest_average(self):
        return max(self._students, key=lambda s: s.average())

    def lowest_average(self):
        return min(self._students, key=lambda s: s.average())

    def class_average(self):
        return sum(s.average() for s in self._students) / len(self._students)

    # Task 7: full report
    def generate_report(self):
        line = "=" * 50
        parts = [line, "STUDENT PERFORMANCE REPORT", line]
        for student in self._students:
            parts.append(student.generate_report())
            parts.append("-" * 50)
        high, low = self.highest_average(), self.lowest_average()
        parts += [
            "CLASS PERFORMANCE SUMMARY",
            f"Highest average : {high.full_name} ({high.average():.2f})",
            f"Lowest average  : {low.full_name} ({low.average():.2f})",
            f"Class average   : {self.class_average():.2f}",
            line,
        ]
        return "\n".join(parts)


# Load students from CSV
def load_students(csv_path, scholarship_students=None):
    scholarship_students = scholarship_students or {}
    students = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            marks = {
                "Math": float(row["Math"]),
                "English": float(row["English"]),
                "Science": float(row["Science"]),
            }
            args = (row["StudentID"], row["FName"], row["LName"], row["Programme"], marks)
            if row["StudentID"] in scholarship_students:
                students.append(ScholarshipStudent(*args, scholarship_students[row["StudentID"]]))
            else:
                students.append(AIUStudent(*args))
    return students


# Main program
if __name__ == "__main__":
    applicants = {"25/224": 50000, "25/228": 75000, "25/230": 40000}
    students = load_students("students.csv", applicants)

    # Task 5: Polymorphism
    print("--- Polymorphism demo: get_status() ---")
    for student in students:
        print(f"{student.full_name:<16} ({type(student).__name__:<18}): {student.get_status()}")

    # Task 6: flexible interface demo
    print("\n--- Flexible average demo ---")
    print("Three marks :", Student.calculate_average(75, 80, 70))
    print("Five marks  :", Student.calculate_average(75, 80, 70, 65, 90))
    try:
        Student.calculate_average(75, 120)
    except ValueError as error:
        print("Validation  :", error)

    # Task 7: full report
    print()
    print(PerformanceAnalyzer(students).generate_report())

    print("""
EXPLANATION
Polymorphism: AIUStudent and ScholarshipStudent both have get_status().
ScholarshipStudent overrides the parent version, so when the loop calls
student.get_status() on a mixed list, Python runs the version that belongs
to each object's actual class (method overriding).

Flexible interface: Python has no traditional overloading, so
calculate_average(*marks) uses variable-length arguments. It accepts three
marks or any number of marks, and validates that there is at least one
mark, that each is a number, and that each is between 0 and 100.
""")