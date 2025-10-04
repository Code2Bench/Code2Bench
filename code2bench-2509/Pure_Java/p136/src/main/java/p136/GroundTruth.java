package p136;
public class GroundTruth {
    public static String getLabelName(int offset) {
        if (offset < 0) {
            return String.format("LB_%x", -offset);
        }
        return String.format("L%x", offset);
    }
}