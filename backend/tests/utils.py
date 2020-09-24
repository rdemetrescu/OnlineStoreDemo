import secrets


def fake_email_generator():
    return f"{secrets.token_hex(10)}@{secrets.token_hex(10)}.com"
