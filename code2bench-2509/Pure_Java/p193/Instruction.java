package p193;

public class Tested {
    /**
     * Calculates the eased value for a circular easing function that transitions smoothly
     * from acceleration to deceleration. This method is typically used in animations to
     * create a more natural motion effect.
     *
     * <p>The easing function is defined as follows:
     * <ul>
     *   <li>For the first half of the duration, the value is calculated using the circular
     *       ease-in formula: {@code -change / 2 * (Math.sqrt(1 - time * time) - 1) + begin}.</li>
     *   <li>For the second half of the duration, the value is calculated using the circular
     *       ease-out formula: {@code change / 2 * (Math.sqrt(1 - time * time) + 1) + begin}.</li>
     * </ul>
     *
     * @param time The current time or progress in the animation, typically between 0 and duration.
     * @param begin The starting value of the property being animated.
     * @param change The total change in the property's value over the duration.
     * @param duration The total duration of the animation.
     * @return The eased value at the specified time, based on the circular easing function.
     * @throws IllegalArgumentException if {@code duration} is zero or negative.
     */
    public static double BLI_easing_circ_ease_in_out(double time, double begin, double change, double duration) {
        // TODO: implement this method
    }
}