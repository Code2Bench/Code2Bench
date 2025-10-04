package p188;
public class GroundTruth {
    public static float calculateCorrelation(float[] data1, float[] data2) {
        if (data1.length != data2.length) {
            throw new IllegalArgumentException("Data sets must be the same length when calculating correlation");
        }
        
        float sum12 = 0;
        float sum1 = 0;
        float sum2 = 0;
        float sum1square = 0;
        float sum2square = 0;
        
        for (int i = 0; i < data1.length; i++) {
            sum12 += data1[i] * data2[i];
            sum1 += data1[i];
            sum2 += data2[i];
            sum1square += data1[i] * data1[i];
            sum2square += data2[i] * data2[i];
        }
        
        float top = sum12 - ((sum1 * sum2) / data1.length);
        float bottomRight = sum2square - ((sum2 * sum2) / data1.length);
        float bottomLeft = sum1square - ((sum1 * sum1) / data1.length);
        float bottom = (float) Math.sqrt(bottomLeft * bottomRight);
        
        return top / bottom;
    }
}