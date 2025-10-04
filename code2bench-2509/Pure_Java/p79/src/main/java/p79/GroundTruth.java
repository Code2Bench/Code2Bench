package p79;
public class GroundTruth {
    public static float[] getClampedAnalogPosition(float x, float y, float lx, float ly) {
        float dx = lx * 30F;
        float dy = ly * 30F;

        float distSquared = dx * dx + dy * dy;
        float maxDist = 30F * 30F;

        if (distSquared > maxDist) {
            float scale = (float) (30F / Math.sqrt(distSquared));
            dx *= scale;
            dy *= scale;
        }

        return new float[] { dx + x, dy + y };
    }
}