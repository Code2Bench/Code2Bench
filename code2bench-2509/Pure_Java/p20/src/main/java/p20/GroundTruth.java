package p20;
public class GroundTruth {
    public static String findLastDigit(String string) {
        for (int i = string.length() - 1; i >= 0; i--) {
            if (Character.isDigit(string.charAt(i))) {
                return String.valueOf(string.charAt(i));
            }
        }
        throw new IllegalArgumentException("No digit found in the string");
    }
}