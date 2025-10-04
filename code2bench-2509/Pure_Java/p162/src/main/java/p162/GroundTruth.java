package p162;
public class GroundTruth {
    public static double offset(double p1, double p2, double a1, double a2, double b1, double b2) {
        double d = 0;

        if (b1 <= p1 || p1 + a1 <= 0) {
            return 0;
        }

        double t = b1 * a2 - a1 * b2;

        if (t > 0) {
            if (p1 < 0) {
                double s = p1 * a2;
                d = s / a1 - p2;
            } else if (p1 > 0) {
                double s = p1 * b2;
                d = s / b1 - p2;
            } else {
                d = -p2;
            }
        } else if (b1 < p1 + a1) {
            double s = (b1 - p1) * a2;
            d = b2 - (p2 + s / a1);
        } else if (b1 > p1 + a1) {
            double s = (a1 + p1) * b2;
            d = s / b1 - (p2 + a2);
        } else {
            d = b2 - (p2 + a2);
        }

        if (d > 0) {
            return d;
        }

        return 0;
    }
}