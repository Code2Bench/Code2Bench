package p247;
public class GroundTruth {
    public static int countNewLines(String str) {
        int count = 0;
        for (int i = 0; i < str.length(); i++) {
            if (str.charAt(i) == '\n') {
                count++;
            }
        }
        return count;
    }
}