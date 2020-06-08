import os


def process_route_id(route_raw):
    """Transforms the big route name into the route_id format of the GTFS data."""

    # Splits on dash
    two_formats = route_raw.split(' - ')
    # First element is the id
    route = two_formats[0]

    # Inserts dash before the two last characters. This normalizes for the GTFS standard.
    route = list(route)
    route.insert(-2, '-')
    route = ''.join(route)

    return route


def process_route_name(route_raw):
    """Transforms the big route name into the human readable name of the route."""

    two_formats = route_raw.split(' - ')
    name = two_formats[1]

    return name
