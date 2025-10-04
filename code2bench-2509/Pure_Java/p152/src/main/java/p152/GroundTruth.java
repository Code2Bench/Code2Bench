package p152;
public class GroundTruth {
    public static String calculateSequence(int patternLength, int sequence) {
        StringBuilder stringBuilder = new StringBuilder();
        int numberLength = Integer.toString(sequence).length();
        if (patternLength > 0) {
            stringBuilder.append(sequence);
            for (int i = 1; i <= (patternLength - numberLength); i++) {
                stringBuilder.insert(0, "0");
            }
        }
        return stringBuilder.toString();
    }
}