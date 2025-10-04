package p191;
public class GroundTruth {
    public static double BLI_easing_back_ease_in_out(double time, double begin, double change, double duration, double overshoot) {
        overshoot *= 1.525f;
        if((time /= duration / 2) < 1.0f) {
            return change / 2 * (time * time * ((overshoot + 1) * time - overshoot)) + begin;
        }
        time -= 2.0f;
        return change / 2 * (time * time * ((overshoot + 1) * time + overshoot) + 2) + begin;
    }
}