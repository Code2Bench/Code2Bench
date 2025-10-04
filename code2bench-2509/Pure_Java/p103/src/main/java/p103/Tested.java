package p103;

import java.lang.StringBuilder;

public class Tested {
    /**
     * Consumes characters from the input string starting at the specified cursor position,
     * appending them to the provided {@link StringBuilder} until a matching quote character
     * is encountered. If the quote character is escaped (i.e., appears twice consecutively),
     * it is treated as a literal quote and appended to the builder. The method returns the
     * index of the character immediately after the closing quote.
     *
     * <p>If the input string does not contain a properly closed quote sequence, an
     * {@link IllegalArgumentException} is thrown.
     *
     * @param string the input string to process, must not be null
     * @param quote the quote character to match, must not be null
     * @param cursor the starting position in the string to begin processing, must be a valid
     *               index within the string
     * @param builder the {@link StringBuilder} to which characters are appended, must not be null
     * @return the index of the character immediately after the closing quote
     * @throws IllegalArgumentException if the input string does not contain a properly closed
     *                                  quote sequence
     * @throws NullPointerException if {@code string}, {@code quote}, or {@code builder} is null
     * @throws IndexOutOfBoundsException if {@code cursor} is out of bounds for the input string
     */
    private static int consumeInQuotes(
            String string, char quote, int cursor, StringBuilder builder) {
        if (string == null || builder == null) {
            throw new NullPointerException("string, quote, or builder cannot be null");
        }
        
        int index = cursor;
        while (index < string.length()) {
            char currentChar = string.charAt(index);
            
            if (currentChar == quote) {
                // Found a closing quote, append it to the builder
                builder.append(quote);
                return index + 1; // Return index after the closing quote
            } else if (currentChar == '\\' && index + 1 < string.length()) {
                // Escaped quote, append it to the builder
                char escapedQuote = string.charAt(index + 1);
                builder.append(escapedQuote);
                index += 2;
            } else {
                // Append the character to the builder
                builder.append(currentChar);
                index++;
            }
        }
        
        // If we exited the loop without finding a closing quote, throw exception
        throw new IllegalArgumentException("Input string does not contain a properly closed quote sequence");
    }
}