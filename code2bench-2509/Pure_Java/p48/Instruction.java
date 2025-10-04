package p48;

import java.util.Objects;

public class Tested {
    /**
     * Converts a byte array into a hexadecimal string representation. Each byte in the array
     * is converted to a two-digit hexadecimal value, and the resulting string is the concatenation
     * of these values. The conversion ensures that each byte is treated as an unsigned value
     * (i.e., values are masked with 0xff to avoid sign extension).
     *
     * @param hash The byte array to convert. Must not be null, but can be empty. If null, a
     *             {@link NullPointerException} is thrown.
     * @return A hexadecimal string representation of the byte array. The length of the string
     *         will be exactly twice the length of the input array. If the input array is empty,
     *         an empty string is returned.
     * @throws NullPointerException if {@code hash} is null.
     */
    public static String convertToHexadecimalString(byte[] hash) {
        // TODO: implement this method
    }
}