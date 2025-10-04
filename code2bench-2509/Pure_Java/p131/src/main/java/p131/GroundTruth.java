package p131;
public class GroundTruth {
    public static int getNewLinePosAfter(String code, int startPos) {
        int pos = code.indexOf('\n', startPos);
        if (pos != -1) {
            // check for '\r\n'
            int prev = pos - 1;
            if (code.charAt(prev) == '\r') {
                return prev;
            }
        }
        return pos;
    }
}