package p248;
public class GroundTruth {
    public static String addNewlineEveryNWords(String input, int n) {
        String[] words = input.split("\\s+");
        StringBuilder result = new StringBuilder();

        for (int i = 0; i < words.length; i++) {
            result.append(words[i]);
            if ((i + 1) % n == 0 && i != words.length - 1) {
                result.append("\n");
            } else if (i != words.length - 1) {
                result.append(" ");
            }
        }

        return result.toString();
    }
}