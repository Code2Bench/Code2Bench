package p115;

public class Tested {
    /**
     * Recursively removes leading and trailing forward slashes ('/') from the given string.
     * If the string starts with a slash, it is removed and the method is called recursively
     * on the remaining substring. If the string ends with a slash, it is removed directly.
     * If the string does not start or end with a slash, it is returned unchanged.
     *
     * @param location the string from which to remove leading and trailing slashes. 
     *                 Must not be null.
     * @return the string with leading and trailing slashes removed, or the original string
     *         if no slashes were present at the start or end.
     * @throws NullPointerException if {@code location} is null.
     */
    private static String stripLeadingTrailingSlash(String location) {
        // TODO: implement this method
    }
}