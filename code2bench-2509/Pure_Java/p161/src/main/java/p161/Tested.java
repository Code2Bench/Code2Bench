package p161;

public class Tested {
    /**
     * Converts a hexadecimal character to its corresponding integer value.
     *
     * <p>This method handles both uppercase ('A'-'F') and lowercase ('a'-'f') hexadecimal
     * characters, as well as numeric characters ('0'-'9'). If the input character is not a valid
     * hexadecimal character, the method returns -1.
     *
     * @param c The character to convert. Must be a valid hexadecimal character (0-9, A-F, or a-f).
     * @return The integer value corresponding to the hexadecimal character, or -1 if the character
     *         is not a valid hexadecimal character.
     */
    public static int dehexchar(char c) {
        if ((c >= '0' && c <= '9') || (c >= 'A' && c <= 'F') || (c >= 'a' && c <= 'f')) {
            return c - '0';
        } else {
            return -1;
        }
    }
}