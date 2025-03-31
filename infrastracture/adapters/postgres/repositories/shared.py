from delivery.core.domain.shared.models import Location


def location_to_db_format(location: Location) -> tuple[int, int]:
    return location.coord_x, location.coord_y


def location_from_db_format(location: tuple[int, int] | list[int]) -> Location:
    return Location(coord_x=location[0], coord_y=location[1])
