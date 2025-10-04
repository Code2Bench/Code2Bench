package p183;

public class Tested {
    /**
     * Enhances the audio sensitivity by mapping the root mean square (RMS) value of the audio signal
     * to a normalized bar height. The method applies a piecewise linear transformation to the RMS value
     * to determine the appropriate bar height, ensuring that quieter sounds are more prominently
     * represented while louder sounds are capped to prevent excessive scaling.
     *
     * <p>The method uses the following RMS thresholds and corresponding transformations:
     * <ul>
     *   <li>RMS ≤ 0.0005: Returns 0.05f (true silence, minimal bar height).</li>
     *   <li>0.0005 < RMS ≤ 0.002: Returns 0.1f + (RMS * 20f) (very quiet, short bars).</li>
     *   <li>0.002 < RMS ≤ 0.008: Returns 0.15f + (RMS * 25f) (quiet speech, low bars).</li>
     *   <li>0.008 < RMS ≤ 0.02: Returns 0.25f + (RMS * 15f) (normal speech, medium bars).</li>
     *   <li>0.02 < RMS ≤ 0.05: Returns 0.4f + (RMS * 8f) (louder speech, taller bars).</li>
     *   <li>0.05 < RMS ≤ 0.1: Returns 0.6f + (RMS * 3f) (loud audio, tall bars).</li>
     *   <li>RMS > 0.1: Returns Math.min(0.95f, 0.8f + (RMS * 1.5f)) (very loud, capped at 95%).</li>
     * </ul>
     *
     * @param rms The root mean square value of the audio signal, must be a non-negative float.
     * @return A float value representing the normalized bar height, ranging from 0.05f to 0.95f.
     */
    public static float enhanceAudioSensitivity(float rms) {
        if (rms <= 0.0005f) {
            return 0.05f;
        } else if (rms <= 0.002f) {
            return 0.1f + (rms * 20f);
        } else if (rms <= 0.008f) {
            return 0.15f + (rms * 25f);
        } else if (rms <= 0.02f) {
            return 0.25f + (rms * 15f);
        } else if (rms <= 0.05f) {
            return 0.4f + (rms * 8f);
        } else if (rms <= 0.1f) {
            return 0.6f + (rms * 3f);
        } else {
            return Math.min(0.95f, 0.8f + (rms * 1.5f));
        }
    }
}