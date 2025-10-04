package p215;

import java.util.Objects;

public class Tested {
    /**
     * Extracts a substring from the provided cookie value based on the specified index, number of cookies,
     * and maximum cookie length. The method calculates the starting position of the substring as the product
     * of the index and the maximum cookie length. If the index corresponds to the last cookie (i.e., 
     * {@code i == numberOfCookies - 1}), the substring includes all remaining characters from the calculated
     * starting position to the end of the string. Otherwise, the substring is limited to the maximum cookie
     * length starting from the calculated position.
     *
     * @param i The index of the cookie to extract, must be non-negative and less than {@code numberOfCookies}.
     * @param numberOfCookies The total number of cookies, must be positive.
     * @param maxCookieLength The maximum length of each cookie, must be positive.
     * @param cookieValue The string containing the cookie values, must not be null and must have sufficient
     *                    length to accommodate the requested substring.
     * @return The extracted substring representing the tokenized cookie value.
     * @throws NullPointerException if {@code cookieValue} is null.
     * @throws IllegalArgumentException if {@code i}, {@code numberOfCookies}, or {@code maxCookieLength} are
     *                                  invalid, or if {@code cookieValue} is too short to accommodate the
     *                                  requested substring.
     */
    public static String extractTokenisedCookieValue(
            final int i, final int numberOfCookies, final int maxCookieLength, final String cookieValue) {
        // Validate input parameters
        if (cookieValue == null) {
            throw new NullPointerException("cookieValue cannot be null");
        }
        if (numberOfCookies <= 0) {
            throw new IllegalArgumentException("numberOfCookies must be positive");
        }
        if (maxCookieLength <= 0) {
            throw new IllegalArgumentException("maxCookieLength must be positive");
        }
        if (i < 0 || i >= numberOfCookies) {
            throw new IllegalArgumentException("i must be non-negative and less than numberOfCookies");
        }

        // Calculate starting position
        int start = i * maxCookieLength;
        
        // Determine the end position
        int end = start + (numberOfCookies > 1 ? maxCookieLength : 0);
        
        // Ensure the cookieValue is long enough
        if (end > cookieValue.length()) {
            throw new IllegalArgumentException("cookieValue is too short to accommodate the requested substring");
        }
        
        // Extract the substring
        return cookieValue.substring(start, end);
    }
}