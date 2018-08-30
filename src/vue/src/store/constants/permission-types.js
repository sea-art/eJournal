const GENERAL_LEVEL_PERMISSIONS = new Set([
    'is_superuser',
    'can_edit_institute',
    'can_add_course'
])

const COURSE_LEVEL_PERMISSIONS = new Set([
    'can_edit_course_roles',
    'can_view_course_participants',
    'can_add_course_participants',
    'can_edit_course',
    'can_delete_course'
])

const ASSIGNMENT_LEVEL_PERMISSIONS = new Set([
    'can_add_assignment',
    'can_edit_assignment',
    'can_view_assignment_participants',
    'can_delete_assignment',
    'can_publish_assignment_grades'
])

const JOURNAL_LEVEL_PERMISSIONS = new Set([
    'can_grade_journal',
    'can_publish_journal_grades',
    'can_edit_journal',
    'can_delete_assignment',
    'can_comment_journal'
])

export const ALL_PERIMSSIONS = new Set([
    ...GENERAL_LEVEL_PERMISSIONS,
    ...COURSE_LEVEL_PERMISSIONS,
    ...ASSIGNMENT_LEVEL_PERMISSIONS,
    ...JOURNAL_LEVEL_PERMISSIONS
])

export const PERMISSION_KEY_LEVELS = new Set([
    'general',
    'course',
    'assignment'
])
