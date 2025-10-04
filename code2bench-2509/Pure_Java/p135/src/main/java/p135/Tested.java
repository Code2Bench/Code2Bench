public class Tested {
    /**
     * Determines whether the specified Unicode code point is printable. A code point is considered
     * printable if it is not a control character, not a whitespace (except for the standard space
     * character ' '), and does not belong to certain Unicode categories such as CONTROL, FORMAT,
     * PRIVATE_USE, SURROGATE, or UNASSIGNED.
     *
     * @param codePoint the Unicode code point to be checked.
     * @return {@code true} if the code point is printable; {@code false} otherwise.
     */
    public static boolean isPrintableCodePoint(int codePoint) {
        // Check if the code point is a control character
        if ((codePoint & 0x00000001) == 0) {
            return false;
        }
        
        // Check if it's a whitespace character (excluding space)
        if (isWhitespace(codePoint)) {
            return false;
        }
        
        // Check if it's a control, format, private use, surrogate, or unassigned character
        if (isControlOrInvalid(codePoint)) {
            return false;
        }
        
        return true;
    }

    private static boolean isWhitespace(int codePoint) {
        return Character.isWhitespace(codePoint);
    }

    private static boolean isControlOrInvalid(int codePoint) {
        return (codePoint >= 0x00000001 && codePoint <= 0x0000001F) || // Control characters
               (codePoint >= 0x00000020 && codePoint <= 0x0000007E) || // Whitespace
               (codePoint >= 0x00000080 && codePoint <= 0x000000FF) || // Surrogates
               (codePoint >= 0x0000FFFE && codePoint <= 0x0000FFFF) || // Surrogates
               (codePoint >= 0x00010000 && codePoint <= 0x00010FFFF); // Unassigned
    }
}