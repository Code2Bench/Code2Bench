package p212;

import java.util.Objects;

public class Tested {
    /**
     * Sanitizes a claim path to ensure it is a valid JSONPath expression. If the claim does not
     * start with a dollar sign (`$`), it is wrapped with `$['` and `']` to denote a JSONPath
     * expression. This ensures that the claim name is properly handled, especially when it contains
     * special characters.
     *
     * @param claim The claim path to sanitize. Must not be null or empty.
     * @return A sanitized JSONPath expression. If the input claim already starts with a dollar sign,
     *         it is returned as-is. Otherwise, it is wrapped with `$['` and `']`.
     * @throws IllegalArgumentException if the input claim is null or empty.
     */
    public static String sanitizeClaimPath(final String claim) {
        if (claim == null || claim.isEmpty()) {
            throw new IllegalArgumentException("Claim cannot be null or empty");
        }

        if (claim.startsWith("$")) {
            return claim;
        } else {
            return "$['" + claim + "']";
        }
    }
}