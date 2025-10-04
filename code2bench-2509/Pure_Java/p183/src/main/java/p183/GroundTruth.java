package p183;
public class GroundTruth {
    public static float enhanceAudioSensitivity(float rms) {
        if (rms <= 0.0005f)
            return 0.05f;
        if (rms <= 0.002f)
            return 0.1f + (rms * 20f);
        if (rms <= 0.008f)
            return 0.15f + (rms * 25f);
        if (rms <= 0.02f)
            return 0.25f + (rms * 15f);
        if (rms <= 0.05f)
            return 0.4f + (rms * 8f);
        if (rms <= 0.1f)
            return 0.6f + (rms * 3f);
        return Math.min(0.95f, 0.8f + (rms * 1.5f));
    }
}