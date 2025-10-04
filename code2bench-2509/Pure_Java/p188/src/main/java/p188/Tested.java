package p188;

import java.util.Objects;

public class Tested {
    /**
     * Calculates the Pearson correlation coefficient between two datasets.
     *
     * <p>The Pearson correlation coefficient measures the linear relationship between two datasets.
     * The result is a value between -1 and 1, where:
     * <ul>
     *   <li>1 indicates a perfect positive linear relationship,</li>
     *   <li>-1 indicates a perfect negative linear relationship,</li>
     *   <li>0 indicates no linear relationship.</li>
     * </ul>
     *
     * <p>Both datasets must be of the same length. If the lengths differ, an {@link IllegalArgumentException}
     * is thrown. Null inputs are not allowed and will result in a {@link NullPointerException}.
     *
     * @param data1 the first dataset, must not be null and must have the same length as {@code data2}
     * @param data2 the second dataset, must not be null and must have the same length as {@code data1}
     * @return the Pearson correlation coefficient between the two datasets
     * @throws IllegalArgumentException if the lengths of {@code data1} and {@code data2} are not equal
     * @throws NullPointerException if either {@code data1} or {@code data2} is null
     */
    public static float calculateCorrelation(float[] data1, float[] data2) {
        if (data1 == null || data2 == null) {
            throw new NullPointerException("Data cannot be null");
        }
        
        if (data1.length != data2.length) {
            throw new IllegalArgumentException("Datasets must have the same length");
        }
        
        float sumX = 0.0f;
        float sumY = 0.0f;
        float sumXY = 0.0f;
        float sumXSquare = 0.0f;
        float sumYSquare = 0.0f;
        
        for (int i = 0; i < data1.length; i++) {
            sumX += data1[i];
            sumY += data2[i];
            sumXY += data1[i] * data2[i];
            sumXSquare += data1[i] * data1[i];
            sumYSquare += data2[i] * data2[i];
        }
        
        float n = data1.length;
        float numerator = sumXY - (sumX * sumY) / (n);
        float denominator = (float) Math.sqrt((sumXSquare - (sumX * sumX) / n) * (sumYSquare - (sumY * sumY) / n));
        
        if (denominator == 0) {
            return 0.0f; // Avoid division by zero
        }
        
        return numerator / denominator;
    }
}