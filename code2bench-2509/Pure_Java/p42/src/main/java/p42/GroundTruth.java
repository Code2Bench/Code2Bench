package p42;
public class GroundTruth {
    public static String trimSlashes(String input) {
        if (input == null) {
            return null;
        }
        return input.replaceAll("^/+|/+$", "");
    }
}