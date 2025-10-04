package p198;

import java.util.Objects;

public class Tested {
    /**
     * Parses a string of space-separated float values into a float array.
     *
     * <p>If the input string is empty, an empty float array is returned. The method splits the input
     * string by spaces and converts each resulting substring into a float value. The order of the
     * values in the input string is preserved in the returned array.
     *
     * @param s the string to parse, which must contain space-separated float values. If null, a
     *     NullPointerException is thrown.
     * @return a float array containing the parsed values. If the input string is empty, an empty
     *     float array is returned.
     * @throws NullPointerException if the input string is null.
     * @throws NumberFormatException if any substring cannot be parsed into a float value.
     */
    private static float[] parseFloatArray(String s) {
        if (s == null) {
            throw new NullPointerException("Input string cannot be null");
        }
        
        String[] parts = s.split("\\s+");
        float[] result = new float[parts.length];
        
        for (int i = 0; i < parts.length; i++) {
            try {
                result[i] = Float.parseFloat(parts[i]);
            } catch (NumberFormatException e) {
                throw new NumberFormatException("Cannot parse float: " + parts[i]);
            }
        }
        
        return result;
    }
}