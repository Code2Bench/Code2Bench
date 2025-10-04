package p230;
public class GroundTruth {
    public static boolean[] expand(boolean[] objs, int i, boolean flag) {
        final int size = objs.length;
        final boolean[] newArrays = new boolean[size + i];
        System.arraycopy(objs, 0, newArrays, flag ? 0 : i, size);
        return newArrays;
    }
}