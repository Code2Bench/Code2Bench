package p217;
public class GroundTruth {
    public static String normalizeID(final String entityId) {
        String normalizedId =
            entityId.toLowerCase().replaceAll("[^a-z0-9_@.-]", "_"); // Replace disallowed characters

        if (normalizedId.length() > 256) {
            normalizedId = normalizedId.substring(0, 256);
        }
        return normalizedId;
    }
}