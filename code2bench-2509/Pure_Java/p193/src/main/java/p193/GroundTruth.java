package p193;
public class GroundTruth {
    public static double BLI_easing_circ_ease_in_out(double time, double begin, double change, double duration) {
        if((time /= duration / 2) < 1.0f) {
            return -change / 2 * (Math.sqrt(1 - time * time) - 1) + begin;
        }
        time -= 2.0f;
        return change / 2 * (Math.sqrt(1 - time * time) + 1) + begin;
    }
}