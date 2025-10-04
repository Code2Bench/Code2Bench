package p189;

import java.util.Objects;

public class Tested {
    /**
     * Compares two URLs for equality, ignoring trailing slashes. This method ensures that both URLs
     * end with a trailing slash before performing the comparison. If either URL does not end with
     * a slash, it is appended with one before the comparison.
     *
     * @param a the first URL to compare, must not be null
     * @param b the second URL to compare, must not be null
     * @return {@code true} if the URLs are equal after ensuring both end with a trailing slash,
     *         {@code false} otherwise
     * @throws NullPointerException if either {@code a} or {@code b} is null
     */
    public static boolean urlEqualsIgnoreSlash(String a, String b) {
        if (a == null || b == null) {
            throw new NullPointerException("Both URLs must not be null");
        }

        // Ensure both URLs end with a trailing slash
        String aWithSlash = a.endsWith("/") ? a : a + "/";
        String bWithSlash = b.endsWith("/") ? b : b + "/";

        return aWithSlash.equals(bWithSlash);
    }
}