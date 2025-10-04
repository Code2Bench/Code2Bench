package p209;
public class GroundTruth {
    public static long computeBound(float initialPos, float velocity, float acceleration,
                                    Long targetTime, Float targetVelocity, int minBound, int maxBound) {
        if (acceleration != 0) {
            final int bound = acceleration > 0 ? maxBound : minBound;

            if (targetTime == null || targetTime < 0) {
                final double tmp = Math.sqrt(
                        2 * acceleration * bound - 2 * acceleration * initialPos
                                + velocity * velocity);

                final double firstTime = (-tmp - velocity) / acceleration;
                if (firstTime > 0) {
                    return (long) firstTime;
                }

                final double secondTime = (tmp - velocity) / acceleration;
                if (secondTime > 0) {
                    return (long) secondTime;
                }

                return Long.MAX_VALUE;
            } else {
                final double time =
                        (bound - initialPos - velocity * targetTime -
                                0.5 * acceleration * targetTime * targetTime +
                                targetVelocity * targetTime) /
                                targetVelocity;

                return time > 0 ? (long) time : Long.MAX_VALUE;
            }
        } else {
            float actualVelocity = targetTime == null ? velocity : targetVelocity;
            final int bound = actualVelocity > 0 ? maxBound : minBound;
            if (actualVelocity != 0) {
                final double time = (bound - initialPos) / actualVelocity;
                return time > 0 ? (long) time : Long.MAX_VALUE;
            } else {
                return Long.MAX_VALUE;
            }
        }
    }
}