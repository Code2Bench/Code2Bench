package p49;
public class GroundTruth {
    public static double convertBytes(long bytes, String targetUnit) {
        double convertedSize = bytes;
        switch (targetUnit) {
            case "KB":
                convertedSize /= 1024;
                break;
            case "MB":
                convertedSize /= (1024 * 1024);
                break;
            case "GB":
                convertedSize /= (1024 * 1024 * 1024);
                break;
            case "TB":
                convertedSize /= (1024L * 1024 * 1024 * 1024);
                break;
            case "PB":
                convertedSize /= (1024L * 1024 * 1024 * 1024 * 1024);
                break;
            default:
                throw new IllegalArgumentException("Unsupported target unit: " + targetUnit);
        }
        return convertedSize;
    }
}