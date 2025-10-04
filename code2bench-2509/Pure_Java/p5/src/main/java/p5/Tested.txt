package p5;

import java.util.Objects;

public class Tested {
    /**
     * Pre-processes a JSON string to ensure it is in a valid format. The method handles null or empty
     * strings by returning an empty JSON object ("{}"). It also trims leading and trailing whitespace
     * from the input string. If the string does not start with '{' or '[', it is wrapped in curly braces
     * to form a JSON object. Additionally, if the string starts with '{' but does not end with '}', or
     * starts with '[' but does not end with ']', the appropriate closing character is appended.
     *
     * @param jsonStr the JSON string to pre-process, may be null or empty
     * @return a valid JSON string, never null; returns "{}" if the input is null or empty
     */
    public static String preProcessJson(String jsonStr) {
        if (jsonStr == null || jsonStr.trim().isEmpty()) {
            return "{}";
        }

        jsonStr = jsonStr.trim();

        if (!jsonStr.startsWith("{") && !jsonStr.startsWith("[")) {
            jsonStr = "{" + jsonStr + "}";
        } else if (jsonStr.startsWith("{") && !jsonStr.endsWith("}")) {
            jsonStr = jsonStr + "}";
        } else if (jsonStr.startsWith("[") && !jsonStr.endsWith("]")) {
            jsonStr = jsonStr + "]";
        }

        return jsonStr;
    }
}