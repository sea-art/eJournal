# import names
# import random
#
# from VLE.models import *
#
#
# print("names.get_full_name()")
# print(names.get_full_name())
#
#
# random_users = []
# for _ in range(100):
#     random_users.append({"username": names.get_full_name(), "type": "SD"})
# for _ in range(3):
#     random_users.append({"username": names.get_full_name(), "type": "TE"})
# for _ in range(10):
#     random_users.append({"username": names.get_full_name(), "type": "TA"})
# for _ in range(5):
#     random_users.append({"username": names.get_full_name(), "type": "EX"})
#
# users = []
# for u in random_users:
#     user = User(username=u["username"], password='pass', group=u["type"])
#     user.save()
#     users.append(user)
#
# print("Created random users")
#
# courses = []
# for c in Course.objects.all():
#     for u in random.sample(users, 75):
#         c.participants.add(u)
#     c.save()
#
# print("Added random users to the courses")

# assignments = []
# for a in assign_examples:
#     assignment = Assignment(name=a["name"])
#     assignment.save()
#     for course in a["courses"]:
#         assignment.course.add(courses[course])
#
#     assignments.append(assignment)
#
# journal = []
# for j in journal_examples:
#     pass
