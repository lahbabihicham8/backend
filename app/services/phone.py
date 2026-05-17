class PhoneValidationResult:
    def __init__(self, valid: bool, e164: str = None, local_number: str = None, error: str = None):
        self.valid = valid
        self.e164 = e164
        self.local_number = local_number
        self.error = error

def normalize_kuwait_phone(phone_raw: str) -> PhoneValidationResult:
    western_digits = phone_raw.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789"))
    cleaned = "".join(char for char in western_digits if char.isdigit() or char == "+")

    if cleaned.startswith("+965"):
        local_number = "".join(char for char in cleaned[4:] if char.isdigit())
    else:
        digits = "".join(char for char in cleaned if char.isdigit())
        if digits.startswith("00965"):
            local_number = digits[5:]
        elif digits.startswith("965"):
            local_number = digits[3:]
        else:
            local_number = digits

    if len(local_number) != 8 or not local_number.isdigit() or local_number[0] not in {"5", "6", "9"}:
        return PhoneValidationResult(False, error="INVALID_PHONE")

    return PhoneValidationResult(True, e164=f"+965{local_number}", local_number=local_number)
