package p200;
public class GroundTruth {
    public static double evaluateOperator(char operator, double x, double y) {
        switch (operator) {
            case '+': return y + x;
            case '-': return y - x;
            case '*': return y * x;
            case '/': return y / x;

            case '^': return Math.pow(y, x); // should not happen here, but oh well
        }
        return 0;
    }
}