package p143;
public class GroundTruth {
    public static String getLine(String content, int pos, int end) {
        if (pos >= content.length()) {
            return "";
        }
        if (end != -1) {
            if (end > content.length()) {
                end = content.length() - 1;
            }
        } else {
            end = pos + 1;
        }
        // get to line head
        int headPos = content.lastIndexOf("\n", pos);
        if (headPos == -1) {
            headPos = 0;
        }
        // get to line end
        int endPos = content.indexOf("\n", end);
        if (endPos == -1) {
            endPos = content.length();
        }
        return content.substring(headPos, endPos);
    }
}