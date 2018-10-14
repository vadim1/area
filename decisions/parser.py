
"""
Get the current, next and previous links based
on a given ordered list of urls
"""
def get_nav(current, urls):
    nav = {
        'current': current,
        'nextUrl': "",
        'previousUrl': "",
    }

    if current in urls:
        current_ndx = urls.index(current)
        max_ndx = len(urls)

        next_ndx = current_ndx + 1
        if next_ndx >= max_ndx:
            next_ndx = max_ndx
            nav['nextUrl'] = ""
        else:
            nav['nextUrl'] = urls[next_ndx]

        previous_ndx = current_ndx - 1
        if previous_ndx < 0:
            previous_ndx = 0
            nav['previousUrl'] = ""
        else:
            nav['previousUrl'] = urls[previous_ndx]

        # print("prev[{0}]: {1}, curr[{2}]: {3}, next[{4}]: {5}"
        #       .format(previous_ndx, nav['previous'],
        #               current_ndx, nav['current'],
        #               next_ndx, nav['next']))
    else:
        print("current: {0} is not in navigation list".format(current))
        print("urls: {0}".format(urls))

    return (nav)

"""
Return the navigation elements based on the request
and a list of ordered urls
"""
def parse_request_path(request, module_urls=[]):
    parts = split_path(request.path)

    """
    if using reverse(), it could return the value in unicode.
    Make sure to convert it back to ASCII so that we can work with it
    """
    decoded_urls = [s.encode('ascii') for s in module_urls]

    module_num = parts['moduleNum']
    section = parts['section']
    step = parts['step']

    if step != "":
        current = section + "/" + step
        current_step = section + "_" + step
        template_path = section + "/" + step + ".html"
    else:
        current = section
        current_step = section
        template_path = section + ".html"

    nav = get_nav(request.path, decoded_urls)

    # template location
    prefix = "module" + str(module_num) + "/"
    # url location
    url_prefix = "/" + str(module_num) + "/"

    # Other meta data
    metadata = {
        'currentStep': current_step,
        'prefix': prefix,
        'requestPath': request.path,
        'templatePath': prefix + template_path,
        'urlPrefix': url_prefix,
    }

    parsed = {}
    # Add the parsed url parts
    parsed.update(parts)
    # Add the navigation parts
    parsed.update(nav)
    parsed.update(metadata)

    return parsed

"""
Split the current path into its component parts
e.g. module, section and step (if present)
"""
def split_path(path):
    parsed = {
        'moduleNum': "0",
        'section': "",
        'step': ""
    }

    """
    if using reverse(), it could return the value in unicode.
    Make sure to convert it back to ASCII so that we can work with it
    """
    parts = [s.encode('ascii') for s in path.split("/")]

    for counter, part in enumerate(parts):
        # print("{0}: {1}".format(counter, part))
        if counter == 1:
            parsed['moduleNum'] = part
        elif counter == 2:
            if part != '/':
                parsed['section'] = part
        elif counter == 3:
            if part != '/':
                parsed['step'] = part

    return (parsed)