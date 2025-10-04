package p255;
public class GroundTruth {
    public static String limitLength(String value, int maxlength, String suffix) {
        String ret = value;
        if (value.length() > maxlength) {
            ret = value.substring(0, maxlength - suffix.length()) + suffix;
        }
        return ret;
    }
}