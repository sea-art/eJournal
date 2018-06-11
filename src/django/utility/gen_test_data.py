from VLE.models import *

users_examples = [
    {"username": "Lars", "type": "SD"},
    {"username": "Zi", "type": "TA"},
    {"username": "Jeroen", "type": "TE"},
    {"username": "Maarten", "type": "SU"}
]
courses_examples = [
    {"name": "Portofolio Academische Vaardigheden", "abbr": "PAV"},
    {"name": "Beeldbewerken", "abbr": "BB"},
    {"name": "Automaten en Formele Talen", "abbr": "AFT"}
]
assign_examples = [
    {"name": "Logboek", "courses": [0, 1, 2]},
    {"name": "colloquium", "courses": [0]},
    {"name": "Verslag", "courses": [0, 1]}
]
journal_examples = [
    {"assigns": [0], "users": [0]},
]

users = []
for u in users_examples:
    user = User(username=u["username"], password='pass', group=u["type"])
    user.save()
    users.append(user)

courses = []
for c in courses_examples:
    course = Course(name=c["name"], abbreviation=c["abbr"])
    course.save()
    course.author.add(users[2])
    course.author.add(users[3])
    courses.append(course)

assignments = []
for a in assign_examples:
    assignment = Assignment(name=a["name"])
    assignment.save()
    for course in a["courses"]:
        assignment.course.add(courses[course])

    assignments.append(assignment)

journal = []
for j in journal_examples:
    pass
