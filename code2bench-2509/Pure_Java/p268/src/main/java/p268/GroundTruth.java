package p268;
public class GroundTruth {
    public static int indexOf(byte[] hay, byte[] needle, int from) {
        outer: for (int i = from; i <= hay.length - needle.length; i++) {
            for (int j = 0; j < needle.length; j++) {
                if (hay[i + j] != needle[j]) continue outer;
            }
            return i;
        }
        return -1;
    }
}