import uuid
import random
import string

from shared_file import sharedFileList

chars = string.ascii_lowercase + ''.join(map(lambda x: str(x), range(1, 9)))

chars2 = string.ascii_letters + ''.join(map(lambda x: str(x), range(1, 9)))

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

def gen_share_id(chars=chars2, n=10) -> str:
    shared_files = sharedFileList()

    # better store the ids then get it one by one, not this way
    while True:
        share_id = ''.join(random.sample(chars, n))
        if len(shared_files.getById(share_id)) == 0:
            break
    return share_id
    


