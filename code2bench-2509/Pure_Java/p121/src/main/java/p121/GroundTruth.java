package p121;
public class GroundTruth {
    public static String sanitize(String input) {
        if (input == null) return "";
        return input
                .replaceAll("[\\\\/:*?\"<>|]", "")
                .replaceAll("[\\p{Cntrl}]", "")
                .replaceAll("\\s+", " ")
                .trim();
    }
}