package p50;

import java.util.Objects;

public class Tested {
    /**
     * Converts a given size from a specified unit to bytes. The supported units are "KB", "MB", "GB", and "TB".
     * The conversion is based on the following multipliers:
     * <ul>
     *   <li>KB: size * 1024</li>
     *   <li>MB: size * 1024 * 1024</li>
     *   <li>GB: size * 1024 * 1024 * 1024</li>
     *   <li>TB: size * 1024L * 1024 * 1024 * 1024</li>
     * </ul>
     *
     * @param size The size to convert, must be a non-negative value.
     * @param unit The unit of the size, case-insensitive. Must be one of "KB", "MB", "GB", or "TB".
     * @return The size converted to bytes.
     * @throws IllegalArgumentException if the unit is not one of the supported values or if the unit is null.
     * @throws NullPointerException if the unit is null.
     */
    public static long convertToBytes(long size, String unit) {
        // TODO: implement this method
    }
}