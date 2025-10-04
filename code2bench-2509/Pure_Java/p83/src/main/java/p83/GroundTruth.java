package p83;
public class GroundTruth {
    public static int findLineStartIdx(int startIdx, String textContent) {
        int newlineIndex = -1;
        for (int i = startIdx; i >= 0; --i) {
            char curChar = textContent.charAt(i);
            if (curChar == '\n' || curChar == '\r') {
                newlineIndex = i;
                break;
            }
        }
        return newlineIndex + 1;
    }
}