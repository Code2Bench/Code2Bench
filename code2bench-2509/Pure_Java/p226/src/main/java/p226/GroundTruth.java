package p226;
public class GroundTruth {
    public static boolean equal(double a, double b, double e) {
        if (a > b)
            return a - b <= e;
        else
            return b - a <= e;
    }
}