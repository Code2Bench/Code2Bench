package p18;
public class GroundTruth {
    public static String formatViewCount(long viewCount) {
        if (viewCount < 1000) {
            return String.valueOf(viewCount);
        } else if (viewCount < 1000000) {
            return String.format("%.1fK", viewCount / 1000.0);
        } else if (viewCount < 1000000000) {
            return String.format("%.1fM", viewCount / 1000000.0);
        } else {
            return String.format("%.1fB", viewCount / 1000000000.0);
        }
    }
}