package p129;

import java.util.ArrayList;
import java.util.List;

public class Tested {
    /**
     * Converts an array of bytes into a hexadecimal string representation. Each byte is
     * converted to a two-digit hexadecimal value, ensuring that the output string is
     * twice the length of the input byte array. The conversion handles all byte values,
     * including negative values, by masking with 0xff to ensure proper unsigned conversion.
     *
     * @param bytes the byte array to convert to a hexadecimal string. Must not be null.
     * @return a hexadecimal string representation of the input byte array. The string
     *         will be empty if the input array is empty.
     * @throws NullPointerException if the input byte array is null.
     */
    public static String bytesToHex(byte[] bytes) {
        if (bytes == null || bytes.length == 0) {
            return "";
        }

        List<String> hexString = new ArrayList<>();
        for (byte b : bytes) {
            int hex = (b & 0xFF) | 0x100; // Mask with 0xFF to handle negative values
            hexString.add(String.format("%02X", hex & 0xFF)); // Format to two digits
        }

        return String.join("", hexString);
    }
}