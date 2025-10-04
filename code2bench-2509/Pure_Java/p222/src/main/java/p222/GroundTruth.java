package p222;
public class GroundTruth {
    public static int copyOverWrite(float[] array, int fromIndex, int toIndex) {
        final int length = array.length;
        if (fromIndex > toIndex || length <= fromIndex || length < toIndex)
            return length;
        System.arraycopy(array, toIndex, array, fromIndex, length - toIndex);
        return length - (toIndex - fromIndex);
    }
}