package p254;

import java.util.StringTokenizer;

public class Tested {
    /**
     * Determines if the simple name of the given input string is "Contract". The simple name is the substring
     * after the last occurrence of the '.' character. If the input does not contain a '.', the entire input
     * is considered as the simple name.
     *
     * @param input The input string to check. Must not be null.
     * @return {@code true} if the simple name of the input is "Contract"; {@code false} otherwise.
     * @throws NullPointerException if the input is null.
     */
    private static boolean hasSimpleNameContract(String input) {
        if (input == null) {
            throw new NullPointerException("Input cannot be null");
        }

        int lastDotIndex = input.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return input.equals("Contract");
        } else {
            return input.substring(lastDotIndex + 1).equals("Contract");
        }
    }
}