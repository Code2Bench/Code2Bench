package p191;

import java.lang.Math;

public class Tested {
    /**
     * Calculates the easing value for a back-in-out easing function, which creates a slight overshoot
     * at the beginning and end of the animation. This method is commonly used in animations to
     * provide a more natural and dynamic motion.
     *
     * <p>The easing function is defined by the formula:
     * <ul>
     *   <li>For the first half of the duration: 
     *       {@code change / 2 * (time * time * ((overshoot + 1) * time - overshoot)) + begin}</li>
     *   <li>For the second half of the duration: 
     *       {@code change / 2 * (time * time * ((overshoot + 1) * time + overshoot) + 2) + begin}</li>
     * </ul>
     *
     * @param time The current time in the animation, typically between 0 and {@code duration}.
     * @param begin The starting value of the animation.
     * @param change The total change in value over the duration of the animation.
     * @param duration The total duration of the animation.
     * @param overshoot The overshoot factor, which controls the amount of overshoot in the easing.
     * @return The eased value at the given time, between {@code begin} and {@code begin + change}.
     * @throws IllegalArgumentException if {@code duration} is zero or negative.
     */
    public static double BLI_easing_back_ease_in_out(double time, double begin, double change, double duration, double overshoot) {
        if (duration <= 0) {
            throw new IllegalArgumentException("Duration must be positive");
        }

        double t = time / duration;
        double t2 = t * t;

        if (t <= 0.5) {
            return change / 2 * (t2 * ((overshoot + 1) * t - overshoot)) + begin;
        } else {
            return change / 2 * (t2 * ((overshoot + 1) * t + overshoot) + 2) + begin;
        }
    }
}