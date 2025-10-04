package p261;
public class GroundTruth {
    public static float[] matrixMult(float[] a, float[] b, int len) {
        int rows = a.length / len;
        int cols = b.length / len;
        
        float[] out = new float[rows * cols];
        
        for (int i = 0; i < rows; i++) {
            for (int k = 0; k < cols; k++) {
                for (int j = 0; j < len; j++) {
                    out[(i * cols) + k] += a[(i * len) + j] * b[(j * cols) + k];
                }
            }
        }
        
        return out;
    }
}