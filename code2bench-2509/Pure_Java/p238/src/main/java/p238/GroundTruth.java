package p238;
public class GroundTruth {
    public static String formatBitrate(int bitrateBits) {
        if (bitrateBits < 1000) {
            return bitrateBits + " bps";
        } else if (bitrateBits < 1000000) {
            return String.format("%.1f kbps", bitrateBits / 1000.0);
        } else {
            return String.format("%.1f Mbps", bitrateBits / 1000000.0);
        }
    }
}