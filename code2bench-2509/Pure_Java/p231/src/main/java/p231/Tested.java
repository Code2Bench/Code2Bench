package p231;

import java.math.BigDecimal;
import java.math.RoundingMode;

public class Tested {
    /**
     * Rounds up the given value to the nearest multiple of the specified interval. 
     * If the interval is zero, the method returns zero. If the value is zero, the method 
     * returns the interval. The method handles negative values by adjusting the interval 
     * to ensure the rounding is performed correctly in the negative direction.
     *
     * @param value The value to be rounded up. Can be positive, negative, or zero.
     * @param interval The interval to which the value should be rounded up. Can be positive, 
     *                 negative, or zero.
     * @return The rounded-up value. Returns zero if the interval is zero, or the interval 
     *         if the value is zero. Otherwise, returns the smallest multiple of the interval 
     *         that is greater than or equal to the value.
     */
    public static long roundUp(long value, long interval) {
        if (interval == 0) {
            return 0;
        }
        
        // Handle the case where value is zero
        if (value == 0) {
            return interval;
        }
        
        // Handle negative values by adjusting the interval
        if (interval < 0) {
            interval = -interval;
            value = -value;
        }
        
        // Calculate the rounded-up value
        long multiple = (value + interval - 1) / interval * interval;
        
        return multiple;
    }
}