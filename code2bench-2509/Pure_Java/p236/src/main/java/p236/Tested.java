package p236;

import java.math.BigDecimal;

public class Tested {
    /**
     * Formats the given size in bytes into a human-readable string representation.
     * The size is converted to the largest possible unit (B, KB, MB, GB) while keeping
     * the value greater than or equal to 1. The output is formatted as follows:
     * <ul>
     *   <li>If the size is less than 1024 bytes, it is returned as "X B" (e.g., "500 B").</li>
     *   <li>If the size is between 1024 and 1,048,575 bytes, it is returned as "X.Y KB" (e.g., "1.5 KB").</li>
     *   <li>If the size is between 1,048,576 and 1,073,741,823 bytes, it is returned as "X.Y MB" (e.g., "2.3 MB").</li>
     *   <li>If the size is 1,073,741,824 bytes or larger, it is returned as "X.YY GB" (e.g., "1.25 GB").</li>
     * </ul>
     *
     * @param size The size in bytes to format. Must be a non-negative value.
     * @return A human-readable string representation of the size, formatted with the appropriate unit.
     */
    public static String formatSize(long size) {
        if (size <= 0) {
            return "0 B";
        }

        long units[] = {1, 1024, 1_048_576, 1_073_741_824};
        String unitsName[] = {"B", "KB", "MB", "GB"};
        
        for (int i = 0; i < units.length; i++) {
            if (size >= units[i]) {
                long value = size / units[i];
                long remainder = size % units[i];
                
                if (remainder == 0) {
                    return value + " " + unitsName[i];
                } else {
                    return new BigDecimal(value).setScale(1, BigDecimal.ROUND_HALF_UP) + "." + new BigDecimal(remainder).setScale(0, BigDecimal.ROUND_HALF_UP) + " " + unitsName[i];
                }
            }
        }
        
        return "0 B";
    }
}