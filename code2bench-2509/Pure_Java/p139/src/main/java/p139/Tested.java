package p139;

import java.util.Formatter;

public class Tested {
    /**
     * Formats the given integer offset into a hexadecimal string representation. If the offset is negative,
     * the method returns a question mark ("?") to indicate an invalid or unknown offset.
     *
     * @param offset The offset to format. Must be a non-negative integer to produce a valid hexadecimal string.
     * @return A string representation of the offset. If the offset is negative, returns "?". Otherwise, returns
     *         the offset in hexadecimal format prefixed with "0x" and padded to four digits (e.g., "0x0001").
     */
    public static String formatOffset(int offset) {
        if (offset < 0) {
            return "?";
        }
        
        StringBuilder sb = new StringBuilder();
        sb.append("0x");
        sb.append(String.format("%04x", offset));
        return sb.toString();
    }
}