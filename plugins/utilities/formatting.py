# smush multiple spaces into one
def compress_whitespace(text):
    whitespace = re.compile(r"\s+")
    return whitespace.sub(' ', text).strip()


# replaces newlines (unix or windows) with a space
def remove_newlines(text, separator=' '):
    lines = re.compile(r"[\r\n]+")
    return whitespace.sub(separator, text).strip()
