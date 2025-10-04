package p244;
public class GroundTruth {
    public static int findEndMarker(byte[] data) {
        for (int i = 4; i < data.length - 1; i++) {
            if (data[i] == 0x24 && data[i + 1] == 0x24) {
                return i;
            }
        }
        return -1;
    }
}