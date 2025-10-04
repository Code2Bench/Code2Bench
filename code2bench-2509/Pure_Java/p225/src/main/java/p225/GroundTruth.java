package p225;
public class GroundTruth {
    public static boolean equal(int a, int b, int epsilon) {
        if (a > b)
            return a - b <= epsilon;
        else
            return b - a <= epsilon;
    }
}