from django import template


register = template.Library()

@register.filter(name='censor')
def censor(text):
    f = open("censor_words.txt", 'r')
    swords = f.read()
    text_split = text.split()

    for word in text_split:
        replaced = ["***" if word in swords else word for word in text_split]
        censored = ' '.join(replaced)
        return censored