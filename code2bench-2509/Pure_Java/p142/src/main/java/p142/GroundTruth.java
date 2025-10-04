package p142;
public class GroundTruth {
    public static int countLinesByPos(String content, int pos, int start) {
        if (start >= pos) {
            return 0;
        }
        int count = 0;
        int tempPos = start;
        do {
            tempPos = content.indexOf("\n", tempPos);
            if (tempPos == -1) {
                break;
            }
            if (tempPos >= pos) {
                break;
            }
            count += 1;
            tempPos += 1;
        } while (tempPos < content.length());
        return count;
    }
}