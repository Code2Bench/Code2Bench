package p229;
public class GroundTruth {
    public static float[] expand(float[] objs, int i, boolean flag) {
        final int size = objs.length;
        final float[] newArrays = new float[size + i];
        System.arraycopy(objs, 0, newArrays, flag ? 0 : i, size);
        return newArrays;
    }
}