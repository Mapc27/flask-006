def password_validation(password):
    return all((
        len(password) > 7,
        any(
            symbol.isupper() for symbol in password
        ),
        len([1 for symbol in password if symbol.isdigit()]) > 1,
    ))
