package p192;

public class Tested {
    /**
     * Calculates the easing value for a bounce effect at the end of a transition.
     * This method implements a bounce easing function that simulates a bouncing motion
     * as the transition nears its end. The easing is applied based on the normalized
     * time, the starting value, the change in value, and the total duration of the transition.
     *
     * The method divides the time by the duration to normalize it, then applies a series
     * of conditions to determine the appropriate easing value. The conditions are based
     * on specific time intervals, each corresponding to a different phase of the bounce
     * effect. The final value is computed by applying a quadratic function to the normalized
     * time and adding the starting value.
     *
     * @param time The current time in the transition, typically between 0 and duration.
     * @param begin The starting value of the transition.
     * @param change The total change in value over the duration of the transition.
     * @param duration The total duration of the transition.
     * @return The eased value at the specified time, calculated using the bounce easing function.
     * @throws IllegalArgumentException if duration is zero or negative.
     */
    public static double BLI_easing_bounce_ease_out(double time, double begin, double change, double duration) {
        // TODO: implement this method
    }
}