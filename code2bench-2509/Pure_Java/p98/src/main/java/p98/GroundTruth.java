package p98;
public class GroundTruth {
    public static boolean isVideoConsideredNew(long timestampMillis) {
        if (timestampMillis <= 0) {
            return false; // Invalid timestamp
        }
        long currentTime = System.currentTimeMillis();
        long twentyFourHoursInMillis = 24 * 60 * 60 * 1000;
        return (currentTime - timestampMillis) < twentyFourHoursInMillis;
    }
}