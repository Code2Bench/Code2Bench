package p200;

import java.util.*;

public class Tested {
    /**
     * Evaluates a binary operation based on the specified operator and operands.
     * 
     * This method performs the following operations based on the provided operator:
     * <ul>
     *   <li>'+': Returns the sum of y and x (y + x).</li>
     *   <li>'-': Returns the difference between y and x (y - x).</li>
     *   <li>'*': Returns the product of y and x (y * x).</li>
     *   <li>'/': Returns the quotient of y divided by x (y / x).</li>
     *   <li>'^': Returns y raised to the power of x (y^x).</li>
     * </ul>
     * 
     * If the operator is not recognized, the method returns 0. Note that the '^' operator
     * is included for completeness, though it is not expected to be used in the context
     * of this method.
     *
     * @param operator The character representing the binary operation to perform. Must be one of '+', '-', '*', '/', or '^'.
     * @param x The second operand in the binary operation.
     * @param y The first operand in the binary operation.
     * @return The result of the binary operation. Returns 0 if the operator is not recognized.
     */
    private static double evaluateOperator(char operator, double x, double y) {
        switch (operator) {
            case '+':
                return y + x;
            case '-':
                return y - x;
            case '*':
                return y * x;
            case '/':
                if (x == 0) {
                    throw new IllegalArgumentException("Division by zero");
                }
                return y / x;
            case '^':
                return Math.pow(y, x);
            default:
                return 0;
        }
    }
}