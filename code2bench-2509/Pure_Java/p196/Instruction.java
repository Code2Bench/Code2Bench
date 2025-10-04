package p196;

public class Tested {
    /**
     * Calculates the eased value for a quart (fourth power) easing function in the "ease-in-out" style.
     * This method is typically used in animations to create smooth transitions. The easing function
     * starts slowly, accelerates in the middle, and then decelerates towards the end.
     *
     * @param time The current time or progress in the animation, typically between 0 and {@code duration}.
     * @param begin The starting value of the animation.
     * @param change The total change in value over the duration of the animation (i.e., {@code end - begin}).
     * @param duration The total duration of the animation.
     * @return The eased value at the specified {@code time}, interpolated between {@code begin} and {@code begin + change}.
     * @throws IllegalArgumentException if {@code duration} is less than or equal to 0.
     */
    public static double BLI_easing_quart_ease_in_out(double time, double begin, double change, double duration) {
        // TODO: implement this method
    }
}