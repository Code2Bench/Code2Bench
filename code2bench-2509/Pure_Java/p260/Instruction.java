package p260;

public class Tested {
    /**
     * Converts a color value represented in a YCbCrK color space to a CMYK color space.
     * The input array is expected to contain four float values representing Y, Cb, Cr, and K components.
     * The method calculates the CMYK values by applying specific transformations to the Y, Cb, and Cr components,
     * while the K component is directly copied to the output array.
     *
     * The calculated CMYK values are clamped to the range [0.0, 1.0] to ensure they are valid color components.
     *
     * @param colorvalue An array of four float values representing the Y, Cb, Cr, and K components of the color.
     *                   The array must not be null and must have exactly four elements.
     * @return An array of four float values representing the CMYK components of the color.
     *         The order of the components in the array is C, M, Y, K.
     * @throws IllegalArgumentException if the input array is null or does not have exactly four elements.
     */
    private static float[] toCmyk(float[] colorvalue) {
        // TODO: implement this method
    }
}