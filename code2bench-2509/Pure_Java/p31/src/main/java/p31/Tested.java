public class Tested {
    /**
     * Converts a given regular expression string into a case-insensitive version by wrapping each
     * alphabetic character in a character class that includes both its lowercase and uppercase forms.
     * Non-alphabetic characters are left unchanged.
     *
     * <p>For example, the input "Hello[0-9]" would be converted to "[hH][eE][lL][lL][oO][0-9]".
     *
     * @param regex the regular expression string to convert. Must not be null.
     * @return a case-insensitive version of the input regular expression string.
     * @throws NullPointerException if the input {@code regex} is null.
     */
    public static String toCaseInsensitiveRegex(String regex) {
        if (regex == null) {
            throw new NullPointerException("Input regex cannot be null");
        }

        StringBuilder result = new StringBuilder();
        int i = 0;
        while (i < regex.length()) {
            char c = regex.charAt(i);
            if (Character.isAlphabetic(c)) {
                // Wrap the character in [ and ] and include both cases
                result.append('[');
                result.append(Character.toLowerCase(c));
                result.append(Character.toUpperCase(c));
                result.append(']');
                i++;
            } else {
                result.append(c);
                i++;
            }
        }
        return result.toString();
    }
}