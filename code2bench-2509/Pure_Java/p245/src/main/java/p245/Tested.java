package p245;

import java.util.*;

public class Tested {
    /**
     * Computes the Levenshtein distance between two strings. The Levenshtein distance is a measure of the
     * difference between two strings, defined as the minimum number of single-character edits (insertions,
     * deletions, or substitutions) required to change one string into the other.
     *
     * <p>This method uses a dynamic programming approach to efficiently compute the distance. It iterates
     * through each character of both strings and calculates the cost of transforming one string into the other.
     *
     * @param s1 The first string to compare. Must not be null.
     * @param s2 The second string to compare. Must not be null.
     * @return The Levenshtein distance between the two strings. The value is non-negative and represents the
     *         minimum number of edits required.
     * @throws NullPointerException if either {@code s1} or {@code s2} is null.
     */
    public static int levenshteinDistance(String s1, String s2) {
        if (s1 == null || s2 == null) {
            throw new NullPointerException("Both strings must not be null");
        }

        int m = s1.length();
        int n = s2.length();

        // Create a 2D array for dynamic programming
        int[][] dp = new int[m + 1][n + 1];

        // Initialize the first row (cost of inserting all characters into an empty string)
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i;
        }

        // Initialize the first column (cost of deleting all characters from a string)
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j;
        }

        // Fill the DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                int cost = (s1.charAt(i - 1) == s2.charAt(j - 1)) ? 0 : 1;
                dp[i][j] = Math.min(dp[i - 1][j] + 1, // Deletion
                                   Math.min(dp[i][j - 1] + 1, // Insertion
                                            dp[i - 1][j - 1] + cost)); // Substitution
            }
        }

        return dp[m][n];
    }
}