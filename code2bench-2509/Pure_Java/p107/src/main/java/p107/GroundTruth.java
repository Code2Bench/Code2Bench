package p107;
public class GroundTruth {
    public static boolean isInteger(String s) {
        boolean isInt = s.length() > 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) < '0' || s.charAt(i) > '9') {
                isInt = false;
                break;
            }
        }
        return isInt;
    }
}