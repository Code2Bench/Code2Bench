package p148;
public class GroundTruth {
    public static String clean(String str) {
        if (str == null || str.isEmpty()) {
            return "";
        }
        String result = str.trim().toLowerCase();
        if (result.charAt(0) == 'v') {
            result = result.substring(1);
        }
        // treat package version as part of version
        result = result.replace('-', '.');
        return result;
    }
}