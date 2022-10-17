from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class TagSlugValidator(validators.RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = (
        "Тег должен содержать буквы латинского алфавита или цифры"
    )
    flags = 0


@deconstructible
class HexColorValidator(validators.RegexValidator):
    regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    message = ("Недопустимый вид Hex тега")
    flag = 0
