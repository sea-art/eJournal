from test.factory.assignment import AssignmentFactory, LtiAssignmentFactory, TemplateAssignmentFactory
from test.factory.instance import InstanceFactory
from test.factory.course import CourseFactory, LtiCourseFactory
from test.factory.user import UserFactory, TeacherFactory, AdminFactory
from test.factory.format import FormatFactory, TemplateFormatFactory
from test.factory.entry import EntryFactory
from test.factory.grade import GradeFactory
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
TemplateAssignment = TemplateAssignmentFactory
Course = CourseFactory
LtiCourse = LtiCourseFactory

Student = UserFactory
Teacher = TeacherFactory
Admin = AdminFactory
Role = RoleFactory

Group = GroupFactory
LtiGroup = LtiGroupFactory

Lti = LtiFactory

Participation = ParticipationFactory
GroupParticipation = GroupParticipationFactory

Journal = JournalFactory
Format = FormatFactory
TemplateFormat = TemplateFormatFactory
Template = TemplateFactory

Entry = EntryFactory
StudentComment = StudentCommentFactory
TeacherComment = TeacherCommentFactory
Grade = GradeFactory
