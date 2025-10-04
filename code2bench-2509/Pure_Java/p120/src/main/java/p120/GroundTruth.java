package p120;
public class GroundTruth {
    public static String extractTitleFromFull(String fullTitle) {
        if (fullTitle == null) return null;
        String[] parts = fullTitle.split(":", 2);
        return parts[0].trim();
    }
}