package p138;
public class GroundTruth {
    public static String cleanObjectName(String obj) {
        if (obj.charAt(0) == 'L') {
            int last = obj.length() - 1;
            if (obj.charAt(last) == ';') {
                return obj.substring(1, last).replace('/', '.');
            }
        }
        return obj;
    }
}