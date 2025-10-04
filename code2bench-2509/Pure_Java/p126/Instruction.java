package p126;

import java.util.Objects;

public class Tested {
    /**
     * Verifies the validity of a bank card number using the Luhn algorithm.
     *
     * <p>The Luhn algorithm is a simple checksum formula used to validate a variety of
     * identification numbers, including credit card numbers. This method processes the
     * card number from right to left, doubling every second digit and subtracting 9
     * from any result greater than 9. The sum of all digits is then checked to see if
     * it is divisible by 10.
     *
     * @param cardNumber the bank card number to verify. Must not be null or empty, and
     *                   should only contain numeric characters.
     * @return {@code true} if the card number is valid according to the Luhn algorithm,
     *         {@code false} otherwise.
     * @throws NullPointerException if {@code cardNumber} is null.
     * @throws IllegalArgumentException if {@code cardNumber} is empty or contains non-numeric
     *                                  characters.
     */
    public static boolean luhnBankCardVerify(String cardNumber) {
        // TODO: implement this method
    }
}