package p93;
public class GroundTruth {
    public static String calculateIncrementalContent(String currentOutput, String lastOutput) {
        if (lastOutput != null && !lastOutput.isEmpty() && currentOutput.startsWith(lastOutput)) {
            return currentOutput.substring(lastOutput.length());
        }
        return currentOutput;
    }
}