def get_required_post_params(post, *keys):
    """
    Gets required post parameters, throwing
    KeyError if not peesent.
    """
    result = []
    for key in keys:
        result.append(post[key])
    return result


def get_optional_post_params(post, *keys):
    """
    Gets optional post parameters, filling
    them as None if not present.
    """
    result = []
    for key in keys:
        if key in post:
            result.append(post[key])
        else:
            result.append(None)
    return result


def keyerror_json(*keys):
    if len(keys) == 1:
        return JsonResponse({'result': '400 Bad Request',
                             'description': 'Field {0} is required but is missing.'.format(keys)},
                            status=400)
    else:
        return JsonResponse({'result': '400 Bad Request',
                             'description': 'Fields {0} are required but one or more are missing.'.format(keys)},
                            status=400)
