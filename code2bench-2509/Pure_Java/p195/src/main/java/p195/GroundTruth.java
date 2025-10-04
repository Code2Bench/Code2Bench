package p195;
public class GroundTruth {
    public static double BLI_easing_quad_ease_in_out(double time, double begin, double change, double duration) {
        if((time /= duration / 2) < 1.0f) {
            return change / 2 * time * time + begin;
        }
        time -= 1.0f;
        return -change / 2 * (time * (time - 2) - 1) + begin;
    }
}