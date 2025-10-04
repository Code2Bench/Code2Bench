package p1;

public class Tested {
    /**
     * Converts a given string to camel case format. The input string is expected to be in snake case
     * (e.g., "example_string") or already in camel case. If the input string contains underscores,
     * it will be split into parts, and each part will be capitalized and concatenated to form the
     * camel case result. If the input string does not contain underscores, only the first character
     * will be capitalized.
     *
     * <p>Special cases:
     * <ul>
     *   <li>If the input string is {@code null} or empty, an empty string is returned.</li>
     *   <li>If the input string does not contain underscores, the first character is capitalized,
     *       and the rest of the string is returned as-is.</li>
     *   <li>Leading, trailing, or consecutive underscores are ignored.</li>
     * </ul>
     *
     * @param name The string to convert to camel case. Can be {@code null} or empty.
     * @return The camel case version of the input string, or an empty string if the input is
     *         {@code null} or empty.
     */
    public static String convertToCamelCase(String name) {
        // TODO: implement this method
    }
}