package p211;
public class GroundTruth {
    public static String limitString(final String message, final int maxLength) {
        if (message.length() > maxLength) {
            return message.substring(0, maxLength).concat("...");
        } else {
            return message;
        }
    }
}