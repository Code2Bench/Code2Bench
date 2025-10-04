package p40;
public class GroundTruth {
    public static int compareNullLast(String s1, String s2) {
        if (s1 == null) {
            if (s2 == null) {
                return 0;
            }
            return -1;
        }
        if (s2 == null) {
            return 1;
        }
        return s1.compareTo(s2);
    }
}