package p190;
public class GroundTruth {
    public static double sqrt3(double d) {
        if(d > 0.000001) {
            return Math.exp(Math.log(d) / 3.0);
        } else if(d > -0.000001) {
            return 0;
        } else {
            return -Math.exp(Math.log(-d) / 3.0);
        }
    }
}