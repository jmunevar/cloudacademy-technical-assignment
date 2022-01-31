#!/usr/bin/env python3

import string
import secrets

if __name__ == "__main__":
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(24))
    print(password)
