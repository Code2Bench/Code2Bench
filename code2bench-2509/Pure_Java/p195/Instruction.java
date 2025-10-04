package p195;

public class Tested {
    /**
     * Calculates the eased value for a quadratic ease-in-out transition.
     * 
     * This method computes the eased value based on the given time, starting value, change in value,
     * and total duration. The easing follows a quadratic curve, which starts slow, accelerates in the
     * middle, and then decelerates towards the end.
     *
     * @param time The current time in the transition, typically between 0 and duration.
     * @param begin The starting value of the transition.
     * @param change The total change in value over the duration of the transition.
     * @param duration The total duration of the transition.
     * @return The eased value at the specified time, between `begin` and `begin + change`.
     * @throws IllegalArgumentException if `duration` is less than or equal to 0.
     */
    public static double BLI_easing_quad_ease_in_out(double time, double begin, double change, double duration) {
        // TODO: implement this method
    }
}