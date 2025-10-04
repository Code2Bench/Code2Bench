package p128;
public class GroundTruth {
    public static float calcEnergy(float[] samples) {
        float sum = 0;
        for (float sample : samples) {
            sum += Math.abs(sample);
        }
        return sum / samples.length;
    }
}