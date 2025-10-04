package p216;
public class GroundTruth {
    public static String normalizeToSixParts(final String cronTrigger) {
        final String[] cronParts = cronTrigger.split(" ");
        if (cronParts.length < 6) {
            return "0 " + cronTrigger;
        } else {
            return cronTrigger;
        }
    }
}