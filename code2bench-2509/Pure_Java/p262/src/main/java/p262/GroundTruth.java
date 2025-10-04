package p262;
public class GroundTruth {
    public static int paeth(int left, int up, int upLeft) {
        int p = left + up - upLeft;
        int pa = Math.abs(p - left);
        int pb = Math.abs(p - up);
        int pc = Math.abs(p - upLeft);
        
        if ((pa <= pb) && (pa <= pc)) {
            return left;
        } else if (pb <= pc) {
            return up;
        } else {
            return upLeft;
        }
    }
}