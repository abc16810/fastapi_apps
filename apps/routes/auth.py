from typing import Callable


def get_current_user_authorizer(*, required: bool = True) -> Callable:  # type: ignore
    return lambda x:x
