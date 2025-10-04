package p50;
public class GroundTruth {
    public static long convertToBytes(long size, String unit) {
        switch (unit.toUpperCase()) {
            case "KB":
                return size * 1024;
            case "MB":
                return size * 1024 * 1024;
            case "GB":
                return size * 1024 * 1024 * 1024;
            case "TB":
                return size * 1024L * 1024 * 1024 * 1024;
            default:
                throw new IllegalArgumentException("Unsupported unit: " + unit);
        }
    }
}