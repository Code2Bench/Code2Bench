package p155;

import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Locale;

public class Tested {
    /**
     * Formats the given file size into a human-readable string with appropriate units.
     * The size is converted to the largest possible unit (bytes, KB, MB, or GB) based on its magnitude.
     * The output is formatted as follows:
     * - If the size is less than 1024, it is displayed in bytes (e.g., "512 字节").
     * - If the size is between 1024 and 1024 * 1024, it is displayed in kilobytes (KB) with two decimal places (e.g., "1.50 KB").
     * - If the size is between 1024 * 1024 and 1024 * 1024 * 1024, it is displayed in megabytes (MB) with two decimal places (e.g., "2.75 MB").
     * - If the size is 1024 * 1024 * 1024 or larger, it is displayed in gigabytes (GB) with two decimal places (e.g., "3.00 GB").
     *
     * @param size The file size in bytes. Must be a non-negative value.
     * @return A formatted string representing the file size with the appropriate unit.
     */
    public static String formatFileSize(long size) {
        if (size < 0) {
            throw new IllegalArgumentException("Size must be non-negative");
        }

        double[] units = {1.0, 1024.0, 1_048_576.0, 1_073_741_824.0, 1_099_511_627_776.0};
        String[] unitNames = {"Byte", "KB", "MB", "GB", "TB"};
        int unitIndex = 0;

        while (unitIndex < units.length && size >= units[unitIndex]) {
            unitIndex++;
        }

        double value = size / units[unitIndex];
        DecimalFormat df = new DecimalFormat("#.##");
        DecimalFormatSymbols ds = new DecimalFormatSymbols(Locale.ENGLISH);
        df.setDecimalFormatSymbols(ds);

        return df.format(value) + " " + unitNames[unitIndex];
    }
}