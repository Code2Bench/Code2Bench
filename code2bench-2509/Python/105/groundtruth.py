

def _int_to_text(num):
    """Helper function to convert an integer to text"""

    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
            "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
            "seventeen", "eighteen", "nineteen"]

    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    if num < 20:
        return ones[num]

    if num < 100:
        return tens[num // 10] + (" " + ones[num % 10] if num % 10 != 0 else "")

    if num < 1000:
        return ones[num // 100] + " hundred" + (" " + _int_to_text(num % 100) if num % 100 != 0 else "")

    if num < 1000000:
        return _int_to_text(num // 1000) + " thousand" + (" " + _int_to_text(num % 1000) if num % 1000 != 0 else "")

    if num < 1000000000:
        return _int_to_text(num // 1000000) + " million" + (" " + _int_to_text(num % 1000000) if num % 1000000 != 0 else "")

    return _int_to_text(num // 1000000000) + " billion" + (" " + _int_to_text(num % 1000000000) if num % 1000000000 != 0 else "")