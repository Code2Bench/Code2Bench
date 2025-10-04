package p228;
public class GroundTruth {
    public static String[] expand(String[] objs, int i, boolean flag) {
        final int size = objs.length;
        final String[] newArrays = new String[size + i];
        System.arraycopy(objs, 0, newArrays, flag ? 0 : i, size);
        return newArrays;
    }
}