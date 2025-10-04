package p219;
public class GroundTruth {
    public static float modUnsigned(float num, float den) {
        float result = (num % den);
        if (result < 0) {
            result += den;
        }
        return result;
    }
}