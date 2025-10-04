package p192;
public class GroundTruth {
    public static double BLI_easing_bounce_ease_out(double time, double begin, double change, double duration) {
        time /= duration;
        if(time < (1 / 2.75f)) {
            return change * (7.5625f * time * time) + begin;
        }
        if(time < (2 / 2.75f)) {
            time -= (1.5f / 2.75f);
            return change * ((7.5625f * time) * time + 0.75f) + begin;
        }
        if(time < (2.5f / 2.75f)) {
            time -= (2.25f / 2.75f);
            return change * ((7.5625f * time) * time + 0.9375f) + begin;
        }
        time -= (2.625f / 2.75f);
        return change * ((7.5625f * time) * time + 0.984375f) + begin;
    }
}