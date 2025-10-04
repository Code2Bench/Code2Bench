package p175;

public class Tested {
    /**
     * Determines if the provided input string representing minutes is invalid.
     * An input is considered invalid if it is a non-empty string that, when parsed as an integer,
     * results in a value less than 0 or greater than 60. Empty strings are considered valid.
     *
     * @param minutesText the string representation of minutes to be checked; may be empty but not null.
     * @return {@code true} if the input is invalid (i.e., parsed minutes are less than 0 or greater than 60),
     *         {@code false} otherwise.
     * @throws NumberFormatException if {@code minutesText} is non-empty and cannot be parsed as an integer.
     */
    public static boolean isInvalidInput(String minutesText) {
        // TODO: implement this method
    }
}