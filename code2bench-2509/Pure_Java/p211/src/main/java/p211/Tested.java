package p211;

import java.util.Objects;

public class Tested {
    /**
     * Limits the length of a given string to a specified maximum length. If the string exceeds
     * the maximum length, it is truncated and an ellipsis ("...") is appended to indicate the
     * truncation. If the string is already within the limit, it is returned unchanged.
     *
     * @param message The string to be limited. Must not be null.
     * @param maxLength The maximum allowed length of the string. Must be a non-negative integer.
     * @return The truncated string with an ellipsis if it exceeds the maximum length, or the
     *         original string if it is within the limit.
     * @throws IllegalArgumentException if {@code maxLength} is negative.
     * @throws NullPointerException if {@code message} is null.
     */
    public static String limitString(final String message, final int maxLength) {
        if (message == null) {
            throw new NullPointerException("message cannot be null");
        }
        if (maxLength < 0) {
            throw new IllegalArgumentException("maxLength must be a non-negative integer");
        }

        int length = message.length();
        if (length <= maxLength) {
            return message;
        } else {
            return message.substring(0, maxLength) + "…";
        }
    }
}