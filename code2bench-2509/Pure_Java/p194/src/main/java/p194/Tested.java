package p194;

import java.lang.Math;

public class Tested {
    /**
     * Calculates the eased value at a given time using a cubic ease-in-out function.
     * This method is typically used in animations to create smooth transitions.
     *
     * The easing function follows these rules:
     * - If the normalized time (time / (duration / 2)) is less than 1, the value is calculated
     *   using the cubic ease-in formula: change / 2 * time^3 + begin.
     * - Otherwise, the value is calculated using the cubic ease-out formula: change / 2 * ((time - 2)^3 + 2) + begin.
     *
     * @param time The current time in the animation, typically in seconds or milliseconds.
     * @param begin The starting value of the animation.
     * @param change The total change in value over the duration of the animation.
     * @param duration The total duration of the animation, typically in the same units as time.
     * @return The eased value at the given time, between begin and begin + change.
     * @throws IllegalArgumentException if duration is zero or negative.
     */
    public static double BLI_easing_cubic_ease_in_out(double time, double begin, double change, double duration) {
        if (duration <= 0) {
            throw new IllegalArgumentException("Duration must be positive");
        }

        double normalizedTime = time / (duration / 2);
        
        if (normalizedTime < 1) {
            return begin + (change / 2) * Math.pow(normalizedTime, 3);
        } else {
            return begin + (change / 2) * (Math.pow(normalizedTime - 2, 3) + 2);
        }
    }
}