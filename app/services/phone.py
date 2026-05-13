import phonenumbers

class PhoneValidationResult:
    def __init__(self, valid: bool, e164: str = None, local_number: str = None, error: str = None):
        self.valid = valid
        self.e164 = e164
        self.local_number = local_number
        self.error = error

def normalize_kuwait_phone(phone_raw: str) -> PhoneValidationResult:
    # Clean string
    cleaned = phone_raw.replace(" ", "").replace("-", "")
    
    # If it doesn't have a plus, try to parse it as a Kuwait number
    if not cleaned.startswith("+"):
        if cleaned.startswith("965"):
            cleaned = "+" + cleaned
        elif cleaned.startswith("00965"):
            cleaned = "+" + cleaned[2:]
        else:
            cleaned = "+965" + cleaned
            
    try:
        parsed = phonenumbers.parse(cleaned, "KW")
        if not phonenumbers.is_valid_number(parsed):
            return PhoneValidationResult(False, error="INVALID_PHONE")
            
        if parsed.country_code != 965:
            return PhoneValidationResult(False, error="NON_KUWAIT_PHONE")
            
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        local_number = str(parsed.national_number)
        
        return PhoneValidationResult(True, e164=e164, local_number=local_number)
        
    except phonenumbers.NumberParseException:
        return PhoneValidationResult(False, error="INVALID_PHONE")
