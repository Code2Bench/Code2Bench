package p158;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Removes a specific field and its associated value from a given description string.
     * The method searches for the field followed by a colon (":") in the description. If found,
     * it removes the field and its value up to the next whitespace or the end of the string.
     *
     * @param field The field to be removed, including the colon (e.g., "due:"). Must not be null.
     * @param duedateDescription The description string from which the field and its value are to be removed. Must not be null.
     * @return The modified description string with the specified field and its value removed. If the field is not found,
     *         the original description string is returned unchanged.
     */
    private static String removeValueFrom(String field, String duedateDescription) {
        // Check if the field is null
        if (field == null) {
            return duedateDescription;
        }

        // Use regular expression to find the field and its value
        Pattern pattern = Pattern.compile("\\b" + Pattern.quote(field) + "\\s*:\\s*(.+)");
        Matcher matcher = pattern.matcher(duedateDescription);

        // If the field is found, remove it
        if (matcher.find()) {
            String newValue = matcher.group(1);
            return duedateDescription.replaceFirst("\\b" + Pattern.quote(field) + "\\s*:\\s*" + newValue, "");
        }

        // If the field is not found, return the original string
        return duedateDescription;
    }
}