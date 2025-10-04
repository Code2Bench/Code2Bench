package p114;

import java.util.StringTokenizer;

public class Tested {
    /**
     * Trims leading and trailing slashes ('/') from the input string. If the input string consists
     * entirely of slashes or is empty, an empty string is returned. The method does not modify
     * slashes within the string, only those at the beginning and end.
     *
     * @param input the string to trim slashes from. If null, the behavior is undefined (assumed
     *              to be non-null based on the implementation).
     * @return the trimmed string with leading and trailing slashes removed, or an empty string
     *         if the input consists entirely of slashes or is empty.
     */
    public static String trimSlashes(String input) {
        if (input == null) {
            return "";
        }

        // Check if the input is empty or consists entirely of slashes
        if (input.isEmpty() || input.charAt(0) == '/' && input.charAt(input.length() - 1) == '/') {
            return "";
        }

        // Trim leading and trailing slashes
        int start = 0;
        while (start < input.length() && input.charAt(start) == '/') {
            start++;
        }
        int end = input.length() - 1;
        while (end >= 0 && input.charAt(end) == '/') {
            end--;
        }

        return input.substring(start, end + 1);
    }
}