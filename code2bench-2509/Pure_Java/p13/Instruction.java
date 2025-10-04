package p13;

import java.util.Objects;

public class Tested {
    /**
     * Cleans a raw JSON string by trimming whitespace and extracting the content between the first '{' and the last '}'.
     * If the input string does not contain a valid JSON object (i.e., it lacks a '{' or '}' or they are in the wrong order),
     * an empty string is returned.
     *
     * @param rawJsonString the raw JSON string to be cleaned; may be null or empty
     * @return the cleaned JSON string, or an empty string if the input does not contain a valid JSON object
     */
    public static String cleanJsonString(String rawJsonString) {
        // TODO: implement this method
    }
}