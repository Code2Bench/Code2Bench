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
        // TODO: implement this method
    }
}