package p208;
public class GroundTruth {
    public static Long computeMillisToReachTarget(Float targetVelocity, float initialVelocity,
                                                  float acceleration) {
        if (targetVelocity != null) {
            if (acceleration != 0f) {
                final long time = (long) ((targetVelocity - initialVelocity) / acceleration);
                return time > 0 ? time : 0;
            } else {
                if (targetVelocity < initialVelocity) {
                    return 0L;
                } else {
                    return null;
                }
            }
        } else {
            return null;
        }
    }
}