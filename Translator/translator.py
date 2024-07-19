from deep_translator import GoogleTranslator


def translator(first, second, text):
    translate = GoogleTranslator(source=first, target=second).translate(text)
    return translate

