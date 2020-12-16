
def get_url(url, location):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""

    if (location.startswith("http://")
        or location.startswith("https://")):
        # Location is an absolute URL.
        url = location
    elif location.startswith("//"):
        # Location is a proto-relative absolute URL.
        url = proto + location
    elif location.startswith("/"):
        # Location is a host-relative absolute path.
        url = proto + "//" + host + location
    else:
        # Location is a path-relative relative path.
        if "/" in path:
            path = path[:path.rindex("/")] + "/" + location
        else:
            path = location
        url = proto + "//" + host + "/" + path

    return url

def _assertEqual(a, b):
    if a != b:
        raise AssertionError(f'{a} != {b}')
    assert a == b

if __name__ == '__main__':
    for (url, location, expected) in (
            # Absolute HTTP
            ('http://old.com/test', 'http://new.com/0', 'http://new.com/0'),

            # Absolute HTTPS
            ('http://old.com/test', 'https://new.com/0', 'https://new.com/0'),

            # Proto-relative
            ('http://old.com/test', '//new.com/0', 'http://new.com/0'),

            # Proto-relative HTTPS
            ('https://old.com/test', '//new.com/0', 'https://new.com/0'),

            # Host-relative w/ single-level original path
            ('http://old.com/test', '/test2', 'http://old.com/test2'),

            # Host-relative w/ single-level, trailing "/" original path
            ('http://old.com/test/', '/test2', 'http://old.com/test2'),

            # Path-relative w/ "/" original path
            ('http://old.com/', '1/2', 'http://old.com/1/2'),

            # Path-relative w/ empty original path
            ('http://old.com', '1/2', 'http://old.com/1/2'),

            # Path-relative w/ single-level original path
            ('http://old.com/0', '1/2', 'http://old.com/1/2'),

            # Path-relative w/ multi-level original path
            ('http://old.com/0/1', '2/3', 'http://old.com/0/2/3'),

            # Path-relative w/ multi-level, trailing "/" original path
            ('http://old.com/0/1/', '2/3', 'http://old.com/0/1/2/3'),
        ):
        _assertEqual(get_url(url, location), expected)
