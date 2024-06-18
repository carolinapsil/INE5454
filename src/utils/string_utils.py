def capitalize_initials(text: str) -> str:
    text_list_capitalized = list(map(lambda word: word.capitalize(), text.split(' ')))

    return ' '.join(text_list_capitalized)
