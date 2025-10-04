package p136;

import java.util.HexFormat;

public class Tested {
    /**
     * Generates a label name based on the provided offset. If the offset is negative, the label name
     * is prefixed with "LB_" followed by the hexadecimal representation of the absolute value of the offset.
     * If the offset is non-negative, the label name is prefixed with "L" followed by the hexadecimal
     * representation of the offset.
     *
     * @param offset The integer offset used to generate the label name. Can be any integer value.
     * @return A string representing the label name, formatted according to the offset's sign and value.
     */
    public static String getLabelName(int offset) {
        if (offset < 0) {
            return "LB_" + HexFormat.of().formatHex(offset + offset);
        } else {
            return "L" + HexFormat.of().formatHex(offset);
        }
    }
}