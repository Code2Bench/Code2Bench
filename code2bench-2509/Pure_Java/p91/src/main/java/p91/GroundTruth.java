package p91;
public class GroundTruth {
    public static boolean isLessThanSecondOfDays(Long firstdTimestamp, Long secondTimestamp) {
        final long gmt8 = 8 * 60 * 60 * 1000;
        final long day = 24 * 60 * 60 * 1000;
        firstdTimestamp = firstdTimestamp + gmt8;
        secondTimestamp = secondTimestamp + gmt8;
        return firstdTimestamp / day < secondTimestamp / day;
    }
}