import uuid
import random
import string

chars = string.ascii_lowercase + ''.join(map(lambda x: str(x), range(1, 9)))


def gen_uuid_str() -> str:
    return str(uuid.uuid4())


def gen_access_token(chars: str = chars, n: int = 4) -> str:
    return ''.join(random.sample(chars, n))


def split_filename(filename: str) -> str:
    parts = filename.rsplit(".", 1)
    if len(parts) == 1:
        return parts[0], ''
    elif len(parts) == 2:
        return parts[0], '.' + parts[1]
