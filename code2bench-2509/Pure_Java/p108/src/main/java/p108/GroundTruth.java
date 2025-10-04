package p108;
public class GroundTruth {
    public static long floor(long a, long b) {
        long r = a % b;
        if (r < 0) {
            return a - r - b;
        } else {
            return a - r;
        }
    }
}