package p260;
public class GroundTruth {
    public static float[] toCmyk(float[] colorvalue) {
        float y = colorvalue[0], cb = colorvalue[1], cr = colorvalue[2], k = colorvalue[3];
        float[] cmyk = new float[4];
        float v;
        v = (float) (1.0 - (y + 1.402 * (cr - 0.5)));
        cmyk[0] = v < 0.0f ? 0.0f : (v > 1.0f ? 1.0f : v);
        v = (float) (1.0 - (y - 0.34414 * (cb - 0.5) - 0.71414 * (cr - 0.5)));
        cmyk[1] = v < 0.0f ? 0.0f : (v > 1.0f ? 1.0f : v);
        v = (float) (1.0 - (y + 1.772 * (cb - 0.5)));
        cmyk[2] = v < 0.0f ? 0.0f : (v > 1.0f ? 1.0f : v);
        cmyk[3] = k;
        return cmyk;
    }
}