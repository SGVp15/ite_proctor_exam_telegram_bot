def transliterate(string: str) -> str:
    # Dict for transliter
    abc = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
           'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
           'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
           'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e',
           'ю': 'u', 'я': 'ya', 'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
           'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N',
           'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H',
           'Ц': 'C', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'y', 'Ь': '', 'Э': 'E',
           'Ю': 'U', 'Я': 'Ya', }
    # ',': '', '?': '', ' ': '_', '~': '', '!': '', '@': '', '#': '',
    # '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '-': '', '=': '', '+': '',
    # ':': '', ';': '', '<': '', '>': '', '\'': '', '"': '', '\\': '', '/': '', '№': '',
    # '[': '', ']': '', '{': '', '}': '', 'ґ': '', 'ї': '', 'є': '', 'Ґ': 'g', 'Ї': 'i',
    # 'Є': 'e', '—': ''}

    # Replace all characters in string
    for key in abc:
        string = string.replace(key, abc[key])
    return string


def transliterate_error(string: str) -> str:
    # Dict for transliter
    abc = {'а': 'a', 'о': 'o', 'с': 'c', 'у': 'y',
           'и': 'u',
           'в': 'b', 'н': 'h', 'р': 'p', 'е': 'e',
           'к': 'k', 'м': 'm', 'т': 't', 'х': 'x',

           'А': 'A', 'О': 'O', 'С': 'C', 'У': 'Y',
           'И': 'U',
           'В': 'B', 'Н': 'H', 'Р': 'P', 'Е': 'E',
           'К': 'K', 'М': 'M', 'Т': 'T', 'Х': 'X',
           }
    # Replace all characters in string
    for key in abc:
        string = string.replace(key, abc[key])
    return string
