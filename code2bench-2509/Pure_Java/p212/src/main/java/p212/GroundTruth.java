package p212;
public class GroundTruth {
    public static String sanitizeClaimPath(final String claim) {
        return claim.startsWith("$") ? claim : "$['" + claim + "']";
    }
}