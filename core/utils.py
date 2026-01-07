import unicodedata

def normalize_input(value: str) -> str:
    """Normalize Unicode input to NFC form."""
    if value is None:
        return value
    return unicodedata.normalize("NFC", value)
