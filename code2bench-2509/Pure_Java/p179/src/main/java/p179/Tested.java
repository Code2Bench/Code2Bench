package p179;

import java.util.Random;

public class Tested {
    /**
     * Generates a random numeric code of the specified length. The code consists of digits
     * from 0 to 9, each digit being randomly generated. The length of the code is determined
     * by the {@code codelength} parameter.
     *
     * <p>If {@code codelength} is less than or equal to 0, an empty string is returned.
     *
     * @param codelength the desired length of the generated code. Must be a non-negative integer.
     * @return a string representing the randomly generated numeric code. If {@code codelength}
     *         is less than or equal to 0, an empty string is returned.
     */
    public static String create(int codelength) {
        if (codelength <= 0) {
            return "";
        }
        
        Random random = new Random();
        StringBuilder code = new StringBuilder();
        
        for (int i = 0; i < codelength; i++) {
            int digit = random.nextInt(10);
            code.append(digit);
        }
        
        return code.toString();
    }
}