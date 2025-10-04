package p187;

import java.util.ArrayList;
import java.util.List;

public class Tested {
    /**
     * Finds the optimal Y-axis interval for a given maximum value. The method calculates the smallest interval
     * that ensures the maximum value divided by the interval is less than or equal to 10. The interval is chosen
     * from a predefined set of divisions: 1, 2, 2.5, and 5, scaled by powers of 10.
     *
     * @param max the maximum value to be used for calculating the optimal interval. Must be a positive number.
     * @return the optimal Y-axis interval as a double value.
     * @throws IllegalArgumentException if {@code max} is less than or equal to 0.
     */
    private static double findOptimalYInterval(double max) {
        if (max <= 0) {
            throw new IllegalArgumentException("Maximum value must be positive");
        }

        // Predefined intervals scaled by powers of 10
        List<Double> intervals = new ArrayList<>();
        intervals.add(1.0);
        intervals.add(2.0);
        intervals.add(2.5);
        intervals.add(5.0);

        // Find the smallest interval where max / interval <= 10
        for (double interval : intervals) {
            if (max / interval <= 10) {
                return interval;
            }
        }

        // If no interval found (should not happen with the given constraints)
        throw new IllegalArgumentException("No valid interval found");
    }
}