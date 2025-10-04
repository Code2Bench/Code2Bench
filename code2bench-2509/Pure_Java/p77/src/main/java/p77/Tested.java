package p77;

import java.lang.StringBuffer;

public class Tested {
    /**
     * Converts the specified integer value to a hexadecimal string representation,
     * ensuring the resulting string has a minimum width by padding with leading zeros
     * if necessary. The hexadecimal string is generated using {@link Integer#toHexString(int)}.
     *
     * <p>If the length of the hexadecimal string is less than {@code minWidth}, leading zeros
     * are appended to the string until the desired width is achieved. If the length of the
     * hexadecimal string is already greater than or equal to {@code minWidth}, no padding
     * is applied.
     *
     * @param value    the integer value to convert to a hexadecimal string. Must be a valid integer.
     * @param minWidth the minimum width of the resulting hexadecimal string. Must be non-negative.
     * @return a hexadecimal string representation of the integer value, padded with leading zeros
     *         to meet the minimum width requirement.
     * @throws IllegalArgumentException if {@code minWidth} is negative.
     */
    public static String toHexString(int value, int minWidth) {
        if (minWidth < 0) {
            throw new IllegalArgumentException("minWidth must be non-negative");
        }

        String hex = Integer.toHexString(value);
        int length = hex.length();

        if (length < minWidth) {
            StringBuilder sb = new StringBuffer();
            for (int i = 0; i < minWidth - length; i++) {
                sb.append('0');
            }
            sb.append(hex);
            return sb.toString();
        } else {
            return hex;
        }
    }
}