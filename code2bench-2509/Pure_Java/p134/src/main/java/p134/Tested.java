public class Tested {
    /**
     * Determines if the specified Unicode code point is a valid identifier part.
     * A code point is considered valid if it is a valid Java identifier part as per
     * {@link Character#isJavaIdentifierPart(int)} or if it represents one of the
     * following characters: '@', '.', '-', '+', '=', '/', or '#'.
     *
     * @param codePoint the Unicode code point to be tested
     * @return {@code true} if the code point is a valid identifier part; {@code false} otherwise
     * @throws IllegalArgumentException if the specified code point is not a valid Unicode code point
     */
    public static boolean isValidIdentifierPart(int codePoint) {
        // Check if the code point is a valid Java identifier part
        if (Character.isJavaIdentifierPart(codePoint)) {
            return true;
        }
        
        // Check for special characters: @, ., -, +, =, /, #
        switch (codePoint) {
            case Character.valueOf('@').getCodePoint():
            case Character.valueOf('.').getCodePoint():
            case Character.valueOf('-').getCodePoint():
            case Character.valueOf('+').getCodePoint():
            case Character.valueOf('=').getCodePoint():
            case Character.valueOf('/').getCodePoint():
            case Character.valueOf('#').getCodePoint():
                return true;
            
            default:
                return false;
        }
    }
}