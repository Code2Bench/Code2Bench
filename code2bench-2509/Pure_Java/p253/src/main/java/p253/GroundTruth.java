package p253;
public class GroundTruth {
    public static int chunkBlockIndexGetY(int index) {
        int y = (index & 0x07FFFFF0) >>> 4;
        if ((index & 0x08000000) != 0) y = -y; // Sign bit set, invert sign
        return y; // 4-28 bits
    }
}