package p157;

import java.util.Objects;

public class Tested {
    /**
     * Extracts the value associated with a specific field from a given description string.
     * The field is expected to be followed by a colon (":") in the description. The value is
     * extracted as the substring starting immediately after the colon and ending at the next
     * whitespace character or the end of the string if no whitespace is found.
     *
     * @param field The field name to search for in the description. Must not be null.
     * @param duedateDescription The description string from which to extract the value. Must not be null.
     * @return The extracted value as a String, or {@code null} if the field is not found in the description.
     * @throws NullPointerException if either {@code field} or {@code duedateDescription} is null.
     */
    public static String getValueFrom(String field, String duedateDescription) {
        // TODO: implement this method
    }
}