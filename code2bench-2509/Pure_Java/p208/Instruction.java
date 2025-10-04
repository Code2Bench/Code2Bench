package p208;

import java.util.Objects;

public class Tested {
    /**
     * Computes the time in milliseconds required to reach the target velocity, given the initial velocity
     * and constant acceleration. The method handles various edge cases, including null target velocity,
     * zero acceleration, and scenarios where the target velocity is already achieved or unreachable.
     *
     * <p>If the target velocity is null, the method returns null, indicating that no computation is possible.
     * If the acceleration is zero, the method checks if the target velocity is less than the initial velocity.
     * If so, it returns 0, indicating that the target velocity is already achieved or cannot be reached.
     * Otherwise, it returns null, indicating that the target velocity cannot be reached with zero acceleration.
     * If the acceleration is non-zero, the method calculates the time required to reach the target velocity
     * and ensures the result is non-negative. If the computed time is negative, it returns 0.
     *
     * @param targetVelocity the target velocity in units per millisecond, or null if not specified
     * @param initialVelocity the initial velocity in units per millisecond
     * @param acceleration the constant acceleration in units per millisecond squared
     * @return the time in milliseconds to reach the target velocity, or null if the target velocity is null
     *         or cannot be reached with the given parameters. Returns 0 if the target velocity is already
     *         achieved or cannot be reached.
     */
    protected static Long computeMillisToReachTarget(Float targetVelocity, float initialVelocity,
                                                    float acceleration) {
        // TODO: implement this method
    }
}