
@api_view(['POST'])
@parser_classes([JSONParser])
def update_format(request):
    """ Update a format
    Arguments:
    request -- the request that was send with
        aID -- the assignments' format to update
        max_points -- the max points possible.
        templates -- the list of templates to bind to the format
        presets -- the list of presets to bind to the format
        unused_templates -- the list of templates that are bound to the template
                            deck, but are not used in presets nor the entry templates.
        removed_presets -- presets to be removed
        removed_templates -- templates to be removed

    Returns a json string for if it is successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        aID, templates, presets = utils.required_params(request.data, "aID", "templates", "presets")
        unused_templates, max_points = utils.required_params(request.data, "unused_templates", "max_points")
        removed_presets, removed_templates = utils.required_params(request.data, "removed_presets", "removed_templates")

    except KeyError:
        return responses.keyerror("aID", "templates", "presets", "unused_templates", "max_points")

    try:
        assignment = Assignment.objects.get(pk=aID)
        format = assignment.format
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment not found.')

    if not permissions.has_assignment_permission(request.user, assignment, 'can_edit_assignment'):
        return responses.forbidden('You are not allowed to edit this assignment.')

    format.max_points = max_points
    format.save()
    template_map = {}
    utils.update_presets(assignment, presets, template_map)
    utils.update_templates(format.available_templates, templates, template_map)
    utils.update_templates(format.unused_templates, unused_templates, template_map)

    # Swap templates from lists if they occur in the other:
    # If a template was previously unused, but is now used, swap it to available templates, and vice versa.
    utils.swap_templates(format.available_templates, unused_templates, format.unused_templates)
    utils.swap_templates(format.unused_templates, templates, format.available_templates)

    utils.delete_presets(format.presetnode_set, removed_presets)
    utils.delete_templates(format.available_templates, removed_templates)
    utils.delete_templates(format.unused_templates, removed_templates)

    return responses.success(payload={'format': serialize.format_to_dict(format)})


@api_view(['POST'])
def update_grade_entry(request):
    """Update the entry grade.

    Arguments:
    request -- the request that was send with
        grade -- the grade
        published -- published
        eID -- the entry id

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        grade, published, eID = utils.required_params(request.data, 'grade', 'published', 'eID')
    except KeyError:
        return responses.keyerror('grade', 'published', 'eID')

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry not found.')

    journal = entry.node.journal
    if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_grade_journal'):
        return responses.forbidden('You cannot grade or publish entries.')

    entry.grade = grade
    entry.published = published
    entry.save()

    if entry.published:
        EntryComment.objects.filter(entry_id=eID).update(published=True)

    if entry.published and journal.sourcedid is not None and journal.grade_url is not None:
        payload = lti_grade.replace_result(journal)
    else:
        payload = dict()

    payload['new_grade'] = entry.grade
    payload['new_published'] = entry.published

    return responses.success(payload=payload)


@api_view(['POST'])
def update_publish_grade_entry(request):
    """Update the grade publish status for one entry.

    Arguments:
    request -- the request that was send with
        eID -- the entry id

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, eID = utils.required_params(request.data, 'published', 'eID')
    except KeyError:
        return responses.keyerror('published', 'eID')

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry not found.')

    journal = entry.node.journal
    if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_publish_journal_grades'):
        return responses.forbidden('You cannot publish entries.')

    entry.published = published
    entry.save()

    if entry.published:
        EntryComment.objects.filter(entry_id=eID).update(published=True)

    if published and journal.sourcedid is not None and journal.grade_url is not None:
        payload = lti_grade.replace_result(journal)
    else:
        payload = dict()

    payload['new_published'] = entry.published
    return responses.success(payload={'new_published': entry.published})


@api_view(['POST'])
def update_publish_grades_assignment(request):
    """Update the grade publish status for whole assignment.

    Arguments:
    request -- the request that was send with
        published -- new published state
        aID -- assignment ID

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, aID = utils.required_params(request.data, 'published', 'aID')
    except KeyError:
        return responses.keyerror('aID')

    try:
        assign = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment not found.')

    if not permissions.has_assignment_permission(request.user, assign, 'can_publish_journal_grades'):
        return responses.forbidden('You cannot publish assignments.')

    utils.publish_all_assignment_grades(assign, published)

    for journ in Journal.objects.filter(assignment=assign):
        if journ.sourcedid is not None and journ.grade_url is not None:
            payload = lti_grade.replace_result(journ)
        else:
            payload = dict()

    payload['new_published'] = published
    return responses.success(payload=payload)


@api_view(['POST'])
def update_publish_grades_journal(request):
    """Update the grade publish status for a journal.

    Arguments:
    request -- the request that was send with
        published -- publish state of grade
        jID -- journal ID

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, jID = utils.required_params(request.data, 'published', 'jID')
    except KeyError:
        return responses.keyerror('published', 'jID')

    try:
        journ = Journal.objects.get(pk=jID)
    except Journal.DoesNotExist:
        return responses.DoesNotExist('Journal')

    if not permissions.has_assignment_permission(request.user, journ.assignment, 'can_publish_journal_grades'):
        return responses.forbidden('You are not allowed to publish journal grades.')

    utils.publish_all_journal_grades(journ, published)

    if journ.sourcedid is not None and journ.grade_url is not None:
        payload = lti_grade.replace_result(journ)
    else:
        payload = dict()

    payload['new_published'] = request.data['published']
    return responses.success(payload=payload)


@api_view(['POST'])
def update_entrycomment(request):
    """
    Update a comment to an entry.

    Arguments:
    request -- the request that was send with
        ecID -- The ID of the entrycomment.
        text -- The updated text.
    Returns a json string for if it is successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        ecID, text = utils.required_params(request.data, "ecID", "text")
    except KeyError:
        return responses.keyerror("ecID")

    try:
        comment = EntryComment.objects.get(pk=ecID)
    except EntryComment.DoesNotExist:
        return responses.not_found('Entrycomment does not exist.')

    if not permissions.has_assignment_permission(request.user, comment.entry.node.journal.assignment,
                                                 'can_comment_journal'):
        return responses.forbidden('You cannot comment on entries.')

    comment.text = text
    comment.save()
    return responses.success()
