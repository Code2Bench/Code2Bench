package p49;

import java.util.Objects;

public class Tested {
    /**
     * Converts a given number of bytes into the specified target unit.
     *
     * <p>The supported target units are: "KB" (kilobytes), "MB" (megabytes), "GB" (gigabytes),
     * "TB" (terabytes), and "PB" (petabytes). The conversion is performed by dividing the
     * number of bytes by the appropriate power of 1024 corresponding to the target unit.
     *
     * @param bytes The number of bytes to convert. Must be a non-negative value.
     * @param targetUnit The target unit for conversion. Must be one of "KB", "MB", "GB", "TB", or "PB".
     * @return The converted size in the specified target unit as a double.
     * @throws IllegalArgumentException If the target unit is not one of the supported units.
     * @throws NullPointerException If the target unit is null.
     */
    public static double convertBytes(long bytes, String targetUnit) {
        if (bytes < 0) {
            throw new IllegalArgumentException("Bytes must be non-negative.");
        }
        if (targetUnit == null || !targetUnit.equals("KB") && !targetUnit.equals("MB") && !targetUnit.equals("GB") && !targetUnit.equals("TB") && !targetUnit.equals("PB")) {
            throw new IllegalArgumentException("Target unit must be one of 'KB', 'MB', 'GB', 'TB', or 'PB'.");
        }

        double result = 0.0;
        long power = 1024;

        switch (targetUnit) {
            case "KB":
                result = bytes / power;
                break;
            case "MB":
                result = bytes / (power * power);
                break;
            case "GB":
                result = bytes / (power * power * power);
                break;
            case "TB":
                result = bytes / (power * power * power * power);
                break;
            case "PB":
                result = bytes / (power * power * power * power * power);
                break;
        }

        return result;
    }
}