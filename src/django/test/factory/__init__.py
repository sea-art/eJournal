from test.factory.assignment import AssignmentFactory, LtiAssignmentFactory, TemplateAssignmentFactory
from test.factory.comment import StudentCommentFactory, TeacherCommentFactory
from test.factory.course import CourseFactory, LtiCourseFactory
from test.factory.entry import EntryFactory
from test.factory.format import FormatFactory, TemplateFormatFactory
from test.factory.grade import GradeFactory
from test.factory.group import GroupFactory, LtiGroupFactory
from test.factory.instance import InstanceFactory
from test.factory.journal import JournalFactory
from test.factory.participation import GroupParticipationFactory, ParticipationFactory
from test.factory.presetnode import EntrydeadlineNodeFactory, ProgressNodeFactory
from test.factory.role import RoleFactory, StudentRoleFactory
from test.factory.template import TemplateAllTypesFactory, TemplateFactory
from test.factory.user import AdminFactory, LtiStudentFactory, TeacherFactory, UserFactory

Instance = InstanceFactory
Assignment = AssignmentFactory
LtiAssignment = LtiAssignmentFactory
TemplateAssignment = TemplateAssignmentFactory
Course = CourseFactory
LtiCourse = LtiCourseFactory

Student = UserFactory
LtiStudent = LtiStudentFactory
Teacher = TeacherFactory
Admin = AdminFactory
Role = RoleFactory
StudentRole = StudentRoleFactory

Group = GroupFactory
LtiGroup = LtiGroupFactory

Participation = ParticipationFactory
GroupParticipation = GroupParticipationFactory

Journal = JournalFactory
Format = FormatFactory
TemplateFormat = TemplateFormatFactory
Template = TemplateFactory
TemplateAllTypes = TemplateAllTypesFactory
ProgressNode = ProgressNodeFactory
EntrydeadlineNode = EntrydeadlineNodeFactory

Entry = EntryFactory
StudentComment = StudentCommentFactory
TeacherComment = TeacherCommentFactory
Grade = GradeFactory
