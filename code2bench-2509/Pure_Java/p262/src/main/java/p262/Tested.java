package p262;

import java.util.*;

public class Tested {
    /**
     * Computes the Paeth predictor for a given set of neighboring pixel values.
     * The Paeth predictor is used in PNG image filtering to predict the value of a pixel
     * based on its left, upper, and upper-left neighbors. The method calculates the
     * predicted value `p` as `left + up - upLeft` and then determines which of the three
     * neighboring values (`left`, `up`, or `upLeft`) is closest to `p` in terms of absolute
     * difference. The closest value is returned as the predictor.
     *
     * @param left The value of the left neighboring pixel.
     * @param up The value of the upper neighboring pixel.
     * @param upLeft The value of the upper-left neighboring pixel.
     * @return The value of the Paeth predictor, which is either `left`, `up`, or `upLeft`,
     *         depending on which is closest to the predicted value `p`.
     */
    protected static int paeth(int left, int up, int upLeft) {
        int p = left + up - upLeft;
        
        int diffLeft = Math.abs(p - left);
        int diffUp = Math.abs(p - up);
        int diffUpLeft = Math.abs(p - upLeft);
        
        if (diffLeft < diffUp && diffLeft < diffUpLeft) {
            return left;
        } else if (diffUp < diffUpLeft) {
            return up;
        } else {
            return upLeft;
        }
    }
}