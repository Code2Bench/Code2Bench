package p248;

import java.util.Objects;

public class Tested {
    /**
     * Adds a newline character every {@code n} words in the input string. Words are defined as sequences of
     * characters separated by whitespace. The newline is inserted after the nth word, and spaces are preserved
     * between words except where a newline is added. If the input string is empty or null, it is returned as is.
     *
     * <p>For example, given the input "one two three four five" and {@code n = 2}, the result would be:
     * "one two\nthree four\nfive".
     *
     * @param input the input string to process; may be null or empty
     * @param n the number of words after which to insert a newline; must be greater than 0
     * @return the modified string with newlines inserted every {@code n} words, or the original string if it is
     *         null or empty
     * @throws IllegalArgumentException if {@code n} is less than or equal to 0
     */
    public static String addNewlineEveryNWords(String input, int n) {
        if (n <= 0) {
            throw new IllegalArgumentException("n must be greater than 0");
        }

        if (input == null || input.isEmpty()) {
            return input;
        }

        StringBuilder result = new StringBuilder();
        String[] words = input.split("\\s+");
        int wordIndex = 0;

        for (int i = 0; i < words.length; i++) {
            result.append(words[wordIndex]);
            if (i < words.length - 1 && (i + 1) % n == 0) {
                result.append("\n");
                wordIndex = i;
            } else {
                wordIndex = i + 1;
            }
        }

        return result.toString();
    }
}