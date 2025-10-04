package p159;

import java.lang.StringBuilder;

public class Tested {
    /**
     * Generates a formatted output statement string that can be used to print the given input string.
     * The method constructs a string in the format "out:print(\"input\")", where the input string is
     * properly escaped to handle double quotes (`"`) and backslashes (`\`). Specifically:
     * - Double quotes are escaped as `\"`.
     * - Backslashes are escaped as `\\`.
     *
     * @param toDisplay the input string to be formatted and included in the output statement. Must not be null.
     * @return a formatted string in the format "out:print(\"escaped_input\")", where `escaped_input` is the
     *         input string with special characters properly escaped.
     * @throws NullPointerException if the input string `toDisplay` is null.
     */
    public static String getOutputStatement(String toDisplay) {
        // TODO: implement this method
    }
}