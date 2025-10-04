package p255;

import java.util.Objects;

public class Tested {
    /**
     * Limits the length of the input string by truncating it and appending a suffix if necessary.
     * If the length of the input string exceeds the specified maximum length, it is truncated
     * to ensure that the resulting string, including the suffix, does not exceed the maximum length.
     * If the input string is already within the limit, it is returned unchanged.
     *
     * @param value The input string to be truncated. Must not be null.
     * @param maxlength The maximum allowed length of the resulting string. Must be greater than or equal to the length of the suffix.
     * @param suffix The suffix to append if truncation occurs. Must not be null.
     * @return The truncated string with the suffix appended if necessary, or the original string if no truncation was required.
     * @throws NullPointerException if either {@code value} or {@code suffix} is null.
     * @throws IllegalArgumentException if {@code maxlength} is less than the length of {@code suffix}.
     */
    public static String limitLength(String value, int maxlength, String suffix) {
        // TODO: implement this method
    }
}