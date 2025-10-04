package p127;
public class GroundTruth {
    public static int getFrameSize(byte[] bytes, int size) {
        if (size == 2) {
            return ((bytes[1] & 0xFF) << 8) | (bytes[0] & 0xFF);
        } else if (size == 4) {
            return ((bytes[3] & 0xFF) << 24) |
                    ((bytes[2] & 0xFF) << 16) |
                    ((bytes[1] & 0xFF) << 8) |
                    (bytes[0] & 0xFF);
        }
        return -1;
    }
}