package p42;

/**
 * Trims leading and trailing slashes ('/') from the input string. If the input is null,
 * the method returns null.
 *
 * @param input the string to trim, may be null
 * @return the input string with leading and trailing slashes removed, or null if the input is null
 */
public static String trimSlashes(String input) {
    if (input == null) {
        return null;
    }
    return input.replaceAll("^/+|/+$", "");
}