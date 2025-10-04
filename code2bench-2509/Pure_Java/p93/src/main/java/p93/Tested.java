package p93;

import java.util.Objects;

public class Tested {
    /**
     * Calculates the incremental content between the current output and the last output.
     * If the last output is not null, not empty, and the current output starts with the last output,
     * the method returns the substring of the current output that follows the last output.
     * Otherwise, the method returns the entire current output.
     *
     * @param currentOutput The current output string, which may contain the last output as a prefix.
     *                      Must not be null.
     * @param lastOutput The last output string, which may be a prefix of the current output.
     *                   Can be null or empty.
     * @return The incremental content of the current output relative to the last output.
     *         If the last output is a prefix of the current output, the substring after the last output is returned.
     *         Otherwise, the entire current output is returned.
     */
    public static String calculateIncrementalContent(String currentOutput, String lastOutput) {
        if (lastOutput == null || lastOutput.isEmpty()) {
            return currentOutput;
        }

        int lastOutputLength = lastOutput.length();
        int currentOutputLength = currentOutput.length();

        // Check if lastOutput is a prefix of currentOutput
        if (currentOutput.startsWith(lastOutput)) {
            return currentOutput.substring(lastOutputLength);
        }

        return currentOutput;
    }
}