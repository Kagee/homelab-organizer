from hlo.models import OrderItem, StockItem, Storage


def sha1_to_object(
    sha1_or_url: str, expected_type: type | None = None
) -> tuple[None | Storage | StockItem | OrderItem, bool]:
    # potentially split on URL
    sha1_or_url = sha1_or_url.split("/")
    # get last element
    sha1 = sha1_or_url[-1].upper()

    if expected_type:
        if o := sha1_is_type(sha1, expected_type):
            return o, True
    else:
        for t in [Storage, StockItem, OrderItem]:
            if o := sha1_is_type(sha1, t):
                return o, True
    return None, False


def sha1_is_type(
    sha1: str,
    obj_type: type,
) -> None | Storage | StockItem | OrderItem:
    try:
        return obj_type.objects.get(sha1_id=sha1.upper())
    except obj_type.DoesNotExist:
        return None
