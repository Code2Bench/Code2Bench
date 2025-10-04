package p227;
public class GroundTruth {
    public static boolean equal(float a, float b, float e) {
        if (a > b)
            return a - b <= e;
        else
            return b - a <= e;
    }
}