package p175;
public class GroundTruth {
    public static boolean isInvalidInput(String minutesText) {
        int minutes = 0;

        if (!minutesText.isEmpty()) {
            minutes = Integer.parseInt(minutesText);
        }

        return minutes < 0 || minutes > 60;
    }
}