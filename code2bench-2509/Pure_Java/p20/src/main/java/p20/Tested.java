package p20;

import java.util.Objects;

/**
 * Finds the last digit in the given string by iterating from the end to the start.
 * The method checks each character to determine if it is a digit using {@link Character#isDigit(char)}.
 * If a digit is found, it is returned as a single-character string. If no digit is found,
 * an {@link IllegalArgumentException} is thrown.
 *
 * @param string the string to search for the last digit; must not be null
 * @return the last digit in the string as a single-character string
 * @throws IllegalArgumentException if no digit is found in the string
 */
private static String findLastDigit(String string) {
    if (string == null) {
        throw new IllegalArgumentException("String cannot be null");
    }

    for (int i = string.length() - 1; i >= 0; i--) {
        if (Character.isDigit(string.charAt(i))) {
            return String.valueOf(string.charAt(i));
        }
    }

    throw new IllegalArgumentException("No digit found in the string");
}