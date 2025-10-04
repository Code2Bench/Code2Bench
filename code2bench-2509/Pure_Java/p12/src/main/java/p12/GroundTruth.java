package p12;
public class GroundTruth {
    public static String formatDuration(long milliseconds) {
        if (milliseconds < 1000) {
            return milliseconds + " ms";
        } else if (milliseconds < 60 * 1000) {
            return String.format("%.2f s", milliseconds / 1000.0);
        } else if (milliseconds < 60 * 60 * 1000) {
            return String.format("%.2f min", milliseconds / (60.0 * 1000.0));
        } else {
            return String.format("%.2f h", milliseconds / (60.0 * 60.0 * 1000.0));
        }
    }
}