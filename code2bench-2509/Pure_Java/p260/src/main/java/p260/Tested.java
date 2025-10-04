package p260;

import java.util.Objects;

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
        if (colorvalue == null || colorvalue.length != 4) {
            throw new IllegalArgumentException("Invalid input array: must be non-null and have exactly four elements");
        }

        float Y = colorvalue[0];
        float Cb = colorvalue[1];
        float Cr = colorvalue[2];
        float K = colorvalue[3];

        // Calculate CMYK components
        float C = (1f - 2f * Y / 255f) / 255f;
        float M = (1f - 2f * Y / 255f) / 255f;
        float Y2 = (1f - 2f * Cr / 255f) / 255f;
        float Y3 = (1f - 2f * Cb / 255f) / 255f;

        float Cm = (1f - 2f * Y2 / 255f) / 255f;
        float Ym = (1f - 2f * Y3 / 255f) / 255f;

        float Cmax = Math.max(C, M, Cm, Ym);
        float Cmin = Math.min(C, M, Cm, Ym);

        float C1 = (Cmax - Cmin) / 255f;
        float M1 = (Cmax - Mmin) / 255f;
        float Y1 = (Cmax - Ymin) / 255f;

        float C2 = (Cmax - Cmin) / 255f;
        float M2 = (Cmax - Mmin) / 255f;
        float Y2 = (Cmax - Ymin) / 255f;

        float C3 = (Cmax - Cmin) / 255f;
        float M3 = (Cmax - Mmin) / 255f;
        float Y3 = (Cmax - Ymin) / 255f;

        float C4 = (Cmax - Cmin) / 255f;
        float M4 = (Cmax - Mmin) / 255f;
        float Y4 = (Cmax - Ymin) / 255f;

        // Clamp values to [0.0, 1.0]
        for (int i = 0; i < 4; i++) {
            if (colorvalue[i] < 0.0f) {
                colorvalue[i] = 0.0f;
            }
            if (colorvalue[i] > 1.0f) {
                colorvalue[i] = 1.0f;
            }
        }

        return colorvalue;
    }
}