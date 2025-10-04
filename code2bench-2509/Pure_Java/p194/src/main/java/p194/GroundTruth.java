package p194;
public class GroundTruth {
    public static double BLI_easing_cubic_ease_in_out(double time, double begin, double change, double duration) {
        if((time /= duration / 2) < 1.0f) {
            return change / 2 * time * time * time + begin;
        }
        time -= 2.0f;
        return change / 2 * (time * time * time + 2) + begin;
    }
}