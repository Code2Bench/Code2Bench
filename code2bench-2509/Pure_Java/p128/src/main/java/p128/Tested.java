package p128;

import java.util.Arrays;

public class Tested {
    /**
     * Calculates the energy of a given array of samples. The energy is defined as the average
     * of the absolute values of the samples. This method iterates through the array, sums the
     * absolute values of each sample, and then divides the sum by the number of samples to
     * compute the average.
     *
     * @param samples An array of float values representing the samples. The array must not be
     *                null or empty; otherwise, the behavior is undefined.
     * @return The calculated energy as a float value, which is the average of the absolute
     *         values of the samples.
     */
    public static float calcEnergy(float[] samples) {
        if (samples == null || samples.length == 0) {
            throw new IllegalArgumentException("Samples cannot be null or empty");
        }

        float sum = 0.0f;
        for (float sample : samples) {
            sum += Math.abs(sample);
        }

        return sum / samples.length;
    }
}