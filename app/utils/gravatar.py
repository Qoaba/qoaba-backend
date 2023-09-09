import hashlib


def generate_random_avatar_url(email: str) -> str:
    email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    avatar_service_base_url = "https://www.gravatar.com/avatar/"
    default_avatar_option = "d=retro"
    avatar_url = f"{avatar_service_base_url}{email_hash}?{default_avatar_option}"

    return avatar_url
