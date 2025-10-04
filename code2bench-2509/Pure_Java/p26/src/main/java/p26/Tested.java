package p26;

import java.text.DecimalFormat;

public class Tested {
    /**
     * Formats the given size in bytes into a human-readable string with an appropriate unit (B, KB, MB, GB, TB).
     * The size is converted to the largest possible unit where the value is greater than or equal to 1.
     * The formatted string includes one decimal place and the corresponding unit.
     *
     * <p>Examples:
     * <ul>
     *   <li>0 → "0 B"</li>
     *   <li>1023 → "1023.0 B"</li>
     *   <li>1024 → "1.0 KB"</li>
     *   <li>1048576 → "1.0 MB"</li>
     * </ul>
     *
     * @param size the size in bytes to format; must be a non-negative value.
     * @return a formatted string representing the size with an appropriate unit.
     */
    public static String formatSize(long size) {
        if (size == 0) {
            return "0 B";
        }

        double[] units = {1, 1024, 1048576, 1073741824, 1099511627776};
        String[] unitNames = {"B", "KB", "MB", "GB", "TB"};

        int unitIndex = 0;
        while (unitIndex < units.length && size >= units[unitIndex]) {
            unitIndex++;
        }

        double value = size / units[unitIndex];
        DecimalFormat df = new DecimalFormat("#.0");
        return df.format(value) + " " + unitNames[unitIndex];
    }
}