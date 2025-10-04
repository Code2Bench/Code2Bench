package p146;

import java.lang.StringIndexOutOfBoundsException;

public class Tested {
    /**
     * Adjusts the given class name to conform to a specific type format. The method processes the class name based on its first character:
     * <ul>
     *   <li>If the class name starts with '[', it is returned as-is, assuming it represents an array type.</li>
     *   <li>If the class name starts with 'L' or 'T', it is returned as-is if it already ends with ';'. Otherwise, the method appends ';' to the end.</li>
     *   <li>For all other cases, the class name is prefixed with 'L' and suffixed with ';' to conform to the expected type format.</li>
     * </ul>
     *
     * @param clsName The class name to be fixed. Must not be null or empty.
     * @return The adjusted class name, conforming to the specified type format.
     * @throws StringIndexOutOfBoundsException if the input string is empty.
     */
    private static String fixType(String clsName) {
        if (clsName == null || clsName.isEmpty()) {
            throw new StringIndexOutOfBoundsException("Input string must not be empty");
        }

        if (clsName.charAt(0) == '[') {
            return clsName;
        } else if (clsName.charAt(0) == 'L' || clsName.charAt(0) == 'T') {
            if (clsName.endsWith(";")) {
                return clsName;
            } else {
                return clsName + ";";
            }
        } else {
            return "L" + clsName + ";";
        }
    }
}