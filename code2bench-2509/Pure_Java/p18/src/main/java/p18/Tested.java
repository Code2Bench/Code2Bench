package p18;

import java.math.BigDecimal;
import java.math.RoundingMode;

public class Tested {
    /**
     * Formats the given view count into a human-readable string representation.
     * The method converts the view count into a more compact format based on its magnitude:
     * - If the view count is less than 1,000, it is returned as a plain number.
     * - If the view count is between 1,000 and 999,999, it is formatted as a number with one decimal place followed by 'K' (e.g., "1.5K").
     * - If the view count is between 1,000,000 and 999,999,999, it is formatted as a number with one decimal place followed by 'M' (e.g., "1.5M").
     * - If the view count is 1,000,000,000 or greater, it is formatted as a number with one decimal place followed by 'B' (e.g., "1.5B").
     *
     * @param viewCount The view count to format. Must be a non-negative long value.
     * @return A formatted string representation of the view count.
     */
    public static String formatViewCount(long viewCount) {
        if (viewCount < 1_000) {
            return String.valueOf(viewCount);
        }
        
        double magnitude = Math.log10(viewCount);
        int exponent = (int) Math.floor(magnitude);
        
        double value = viewCount / Math.pow(10, exponent);
        
        if (exponent == 3) {
            return String.format("%.1fB", value);
        } else if (exponent == 6) {
            return String.format("%.1fM", value);
        } else if (exponent == 9) {
            return String.format("%.1fK", value);
        } else {
            return String.format("%.1f", value);
        }
    }
}