package p11;

import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

public class Tested {
    /**
     * Formats a given file size in bytes into a human-readable string representation.
     * The method converts the size into the most appropriate unit (B, KB, MB, or GB)
     * based on the magnitude of the input value. The output is formatted to two decimal
     * places for sizes larger than 1024 bytes.
     *
     * <p>The conversion logic is as follows:
     * <ul>
     *   <li>If the size is less than 1024 bytes, it is returned as "X B" (e.g., "500 B").</li>
     *   <li>If the size is between 1024 and 1024 * 1024 bytes, it is converted to kilobytes (KB)
     *       and formatted as "X.XX KB" (e.g., "1.23 KB").</li>
     *   <li>If the size is between 1024 * 1024 and 1024 * 1024 * 1024 bytes, it is converted to
     *       megabytes (MB) and formatted as "X.XX MB" (e.g., "5.67 MB").</li>
     *   <li>If the size is 1024 * 1024 * 1024 bytes or larger, it is converted to gigabytes (GB)
     *       and formatted as "X.XX GB" (e.g., "2.34 GB").</li>
     * </ul>
     *
     * @param bytes The file size in bytes. Must be a non-negative value.
     * @return A formatted string representing the file size in the most appropriate unit.
     * @throws IllegalArgumentException if the input value is negative.
     */
    public static String formatFileSize(long bytes) {
        if (bytes < 0) {
            throw new IllegalArgumentException("File size cannot be negative");
        }

        double fileSize = (double) bytes / 1024.0;
        int unit = 0;

        if (bytes < 1024) {
            unit = 0;
        } else if (bytes < 1024 * 1024) {
            unit = 1;
        } else if (bytes < 1024 * 1024 * 1024) {
            unit = 2;
        } else {
            unit = 3;
        }

        BigDecimal bigDecimal = new BigDecimal(String.valueOf(fileSize));
        BigDecimal rounded = bigDecimal.setScale(2, BigDecimal.ROUND_HALF_UP);

        DecimalFormat df = new DecimalFormat("#.##");
        if (unit == 0) {
            return df.format(fileSize) + " B";
        } else if (unit == 1) {
            return df.format(fileSize) + " KB";
        } else if (unit == 2) {
            return df.format(fileSize) + " MB";
        } else {
            return df.format(fileSize) + " GB";
        }
    }
}