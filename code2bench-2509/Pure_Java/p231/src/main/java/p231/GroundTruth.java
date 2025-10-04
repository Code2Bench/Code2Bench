package p231;
public class GroundTruth {
    public static long roundUp(long value, long interval) {
        if (interval == 0L) {
            return 0L;
        } else if (value == 0L) {
            return interval;
        } else {
            if (value < 0L) {
                interval *= -1L;
            }

            long remainder = value % interval;

            return remainder == 0L ? value : value + interval - remainder;
        }
    }
}