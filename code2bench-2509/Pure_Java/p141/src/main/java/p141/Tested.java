public class Tested {
    /**
     * Removes all occurrences of the specified character from the given string.
     * If the character is not found in the string, the original string is returned.
     * The method uses a {@link StringBuilder} to efficiently construct the result
     * by iterating through the string and appending non-matching characters.
     *
     * @param str the input string from which the character is to be removed. Must not be null.
     * @param ch the character to be removed from the string.
     * @return a new string with all occurrences of the specified character removed.
     *         If the character is not found, the original string is returned.
     * @throws NullPointerException if the input string {@code str} is null.
     */
    public static String removeChar(String str, char ch) {
        if (str == null) {
            throw new NullPointerException("Input string cannot be null");
        }

        StringBuilder result = new StringBuilder();
        for (char c : str.toCharArray()) {
            if (c != ch) {
                result.append(c);
            }
        }
        return result.toString();
    }
}