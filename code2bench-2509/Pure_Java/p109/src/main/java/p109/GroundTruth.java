package p109;
public class GroundTruth {
    public static long powerX(long a, long b) {
        long x = 1;
        while (b > 0) {
            x *= a;
            --b;
        }
        return x;
    }
}