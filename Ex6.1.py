class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.avg_grades = -1

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lec(self, teacher, course, grade):
        if (isinstance(teacher, Lecturer) and course in teacher.courses_attached
                and (course in self.courses_in_progress or course in self.finished_courses)):
            if course in teacher.grades:
                teacher.grades[course] += [grade]
            else:
                teacher.grades[course] = [grade]
            temp_grades = []
            temp_sum = 0
            for i in teacher.grades.keys():
                temp_grades += teacher.grades.get(i)
            for i in temp_grades:
                temp_sum = temp_sum + i
            teacher.avg_grades = temp_sum / len(temp_grades)
        else:
            return 'Ошибка'

    def __lt__(self, other):
        if not isinstance(other, Student):
            print(f"Ошибка {other.name} {other.surname} - не студент!")
            return
        else:
            return self.avg_grades < other.avg_grades

    def __str__(self):
        if self.avg_grades == -1:
            txt_avg = 'Оценок за домашние задания не имеет.'
        else:
            txt_avg = f'Средняя оценка за домашние задания: {self.avg_grades}'

        if not self.courses_in_progress:
            txt_progress = 'На данный момент не проходит никаких курсов.'
        else:
            txt_progress = f'Курсы в процессе изучения: {", ".join(str(x) for x in self.courses_in_progress)}'

        if not self.finished_courses:
            txt_finish = 'Не имеет завершенных курсов.'
        else:
            txt_finish = f'Завершенные курсы: {", ".join(str(x) for x in self.finished_courses)}'
        return f'Имя: {self.name} \nФамилия: {self.surname} \n{txt_avg} \n{txt_progress} \n{txt_finish}'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}
        self.avg_grades = -1

    def __str__(self):
        if self.avg_grades == -1:
            return f'Имя: {self.name} \nФамилия: {self.surname} \nОценок за лекции не имеет.'
        else:
            return f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self.avg_grades}'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print(f"Ошибка {other.name} {other.surname} - не лектор!")
            return
        else:
            return self.avg_grades < other.avg_grades


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
            temp_grades = []
            temp_sum = 0
            for i in student.grades.keys():
                temp_grades += student.grades.get(i)
            for i in temp_grades:
                temp_sum = temp_sum + i
            student.avg_grades = temp_sum / len(temp_grades)
        else:
            return 'Ошибка'

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'


def avg_students(students, course):
    for i in students:
        if not isinstance(i, Student):
            return f'Ошибка - {i.name} {i. surname} не студент!'
    temp_grades = []
    temp_sum = 0
    empty_flag = 0
    empty_students = []
    for i in students:
        if course in i.grades.keys():
            temp_grades += i.grades.get(course)
        else:
            empty_flag += 1
            empty_students += [f'{i.name} {i.surname}']
    for i in temp_grades:
        temp_sum = temp_sum + i
    if not temp_grades:
        return 'Ни один из студентов еще не имеет оценок'
    elif empty_flag == 0:
        return f'Средняя оценка перечисленных студентов по курсу {course}: {temp_sum / len(temp_grades)}'
    else:
        txt_empty = f"Эти студенты не были учтены, так как не имеют оценок: {', '.join(str(x) for x in empty_students)}"
        return f"Средняя оценка перечисленных студентов по курсу {course}: {temp_sum / len(temp_grades)}.\n{txt_empty}"


def avg_lecturers(teachers, course):
    for i in teachers:
        if not isinstance(i, Lecturer):
            return f'Ошибка - {i.name} {i. surname} не лектор!'
    temp_grades = []
    temp_sum = 0
    empty_flag = 0
    empty_teachers = []
    for i in teachers:
        if course in i.grades.keys():
            temp_grades += i.grades.get(course)
        else:
            empty_flag += 1
            empty_teachers += [f'{i.name} {i.surname}']
    for i in temp_grades:
        temp_sum = temp_sum + i
    if not temp_grades:
        return 'Ни один из лекторов еще не имеет оценок'
    elif empty_flag == 0:
        return f'Средняя оценка перечисленных лекторов по курсу {course}: {temp_sum / len(temp_grades)}'
    else:
        txt_empty = f"Эти лекторы не были учтены, так как не имеют оценок: {', '.join(str(x) for x in empty_teachers)}"
        return f"Средняя оценка перечисленных лекторов по курсу {course}: {temp_sum / len(temp_grades)}.\n{txt_empty}"


PogreevV = Student('Василий', 'Погреев', 'м')
PogreevV.add_courses('Git')
PogreevV.courses_in_progress += ['Python']

IvanovI = Student('Иван', 'Иванов', 'м')
IvanovI.courses_in_progress += ['Python', 'Git']

BulyginO = Lecturer('Олег', 'Булыгин')
BulyginO.courses_attached += ['Python']
IvanovI.rate_lec(BulyginO, 'Python', 10)

GilyazovI = Lecturer('Ильназ', 'Гильязов')
GilyazovI.courses_attached += ['Git']
IvanovI.rate_lec(GilyazovI, 'Python', 10)
PogreevV.rate_lec(GilyazovI, 'Git', 10)

VoronovP = Reviewer('Филипп', 'Воронов')
VoronovP.courses_attached += ['Python']
PogreevV.rate_lec(VoronovP, 'Git', 10)
VoronovP.rate_hw(PogreevV, 'Python', 10)
VoronovP.rate_hw(IvanovI, 'Git', 10)

BatitskayaA = Reviewer('Алёна', 'Батицкая')
BatitskayaA.courses_attached += ['Git']
PogreevV.rate_lec(BatitskayaA, 'Git', 10)
BatitskayaA.rate_hw(PogreevV, 'Python', 10)
BatitskayaA.rate_hw(IvanovI, 'Git', 10)

print(PogreevV, '\n')
print(IvanovI, '\n')
print(BulyginO, '\n')
print(GilyazovI, '\n')
print(VoronovP, '\n')
print(BatitskayaA, '\n')
print(avg_students([IvanovI, PogreevV], 'Git'), '\n')
print(avg_lecturers([BulyginO, GilyazovI], 'Python'), '\n')
print(PogreevV < IvanovI, '\n')
print(PogreevV < BulyginO, '\n')
print(BulyginO < GilyazovI, '\n')