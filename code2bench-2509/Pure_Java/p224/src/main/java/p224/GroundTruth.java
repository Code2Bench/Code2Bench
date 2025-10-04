package p224;
public class GroundTruth {
    public static int modUnsigned(int num, int den) {
        int result = (num % den);
        if (result < 0) {
            result += den;
        }
        return result;
    }
}