package p139;
public class GroundTruth {
    public static String formatOffset(int offset) {
        if (offset < 0) {
            return "?";
        }
        return String.format("0x%04x", offset);
    }
}