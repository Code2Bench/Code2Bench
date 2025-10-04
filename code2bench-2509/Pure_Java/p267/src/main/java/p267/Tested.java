package p267;

import java.util.Objects;

public class Tested {
    /**
     * Converts a 4-character string into a 32-bit integer tag representation.
     * The tag is constructed by shifting each character's ASCII value into its respective
     * byte position within the integer. The first character occupies the most significant byte,
     * and the fourth character occupies the least significant byte.
     *
     * <p>For example, the string "ABCD" is converted to the integer 0x41424344, where:
     * <ul>
     *   <li>'A' (0x41) is shifted to the most significant byte (24 bits left)</li>
     *   <li>'B' (0x42) is shifted to the second byte (16 bits left)</li>
     *   <li>'C' (0x43) is shifted to the third byte (8 bits left)</li>
     *   <li>'D' (0x44) occupies the least significant byte</li>
     * </ul>
     *
     * @param tag The 4-character string to convert. Must not be null and must have exactly 4 characters.
     * @return The 32-bit integer representation of the tag.
     * @throws IllegalArgumentException If the input string is null or does not have exactly 4 characters.
     */
    public static int stringToTag(String tag) {
        if (tag == null || tag.length() != 4) {
            throw new IllegalArgumentException("Tag must be exactly 4 characters long and not null");
        }

        int result = 0;
        for (int i = 0; i < 4; i++) {
            char c = tag.charAt(i);
            int byteValue = (int) c;
            result = (result << 8) | byteValue;
        }

        return result;
    }
}