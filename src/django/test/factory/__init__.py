from test.factory.assignment import AssignmentFactory, LtiAssignmentFactory, GroupAssignment
from test.factory.instance import InstanceFactory
from test.factory.course import CourseFactory, LtiCourseFactory
from test.factory.user import UserFactory, TeacherFactory, AdminFactory
from test.factory.format import FormatFactory
from test.factory.entry import EntryFactory
from test.factory.template import TemplateFactory
from test.factory.group import GroupFactory, LtiGroupFactory
from test.factory.lti import LtiFactory
from test.factory.comment import StudentCommentFactory, TeacherCommentFactory
from test.factory.participation import ParticipationFactory, GroupParticipationFactory
from test.factory.role import RoleFactory
from test.factory.journal import JournalFactory

Instance = InstanceFactory
Assignment = AssignmentFactory
LtiAssignment = LtiAssignmentFactory
GroupAssignment = GroupAssignmentFactory
Course = CourseFactory
LtiCourse = LtiCourseFactory

Student = UserFactory
Teacher = TeacherFactory
Admin = AdminFactory
Role = RoleFactory

Format = FormatFactory
Template = TemplateFactory

Group = GroupFactory
LtiGroup = LtiGroupFactory

Lti = LtiFactory

Participation = ParticipationFactory
GroupParticipation = GroupParticipationFactory

Journal = JournalFactory
Fromat = FormatFactory
Template = TemplateFactory

Entry = EntryFactory
StudentComment = StudentCommentFactory
TeacherComment = TeacherCommentFactory
