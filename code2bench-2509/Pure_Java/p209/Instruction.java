package p209;

import java.util.Objects;

public class Tested {
    /**
     * Computes the time required to reach a specified bound based on initial position, velocity, acceleration,
     * and optional target time and target velocity. The method calculates the time using kinematic equations
     * and adjusts for the direction of acceleration and velocity.
     *
     * <p>If acceleration is non-zero, the method calculates the time to reach the bound using the quadratic
     * kinematic equation. If acceleration is zero, it uses the linear kinematic equation. The method handles
     * edge cases such as null or negative target time, zero velocity, and zero acceleration by returning
     * {@link Long#MAX_VALUE} when the bound cannot be reached.
     *
     * @param initialPos     The initial position (must be a finite float value).
     * @param velocity       The initial velocity (must be a finite float value).
     * @param acceleration   The acceleration (must be a finite float value).
     * @param targetTime     The target time (can be null or a non-negative value). If null or negative, the
     *                       method calculates the time without considering a target time.
     * @param targetVelocity The target velocity (can be null or a finite float value). If null, the method
     *                       uses the initial velocity.
     * @param minBound       The minimum bound (must be an integer).
     * @param maxBound       The maximum bound (must be an integer).
     * @return The time required to reach the bound, or {@link Long#MAX_VALUE} if the bound cannot be reached.
     * @throws NullPointerException if {@code initialPos}, {@code velocity}, or {@code acceleration} is null.
     */
    protected static long computeBound(float initialPos, float velocity, float acceleration,
                                       Long targetTime, Float targetVelocity, int minBound, int maxBound) {
        // TODO: implement this method
    }
}