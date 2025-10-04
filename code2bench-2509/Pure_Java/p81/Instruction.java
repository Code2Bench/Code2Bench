package p81;

import java.util.Objects;

public class Tested {
    /**
     * Creates a regex pattern for matching a given type name, handling both simple and fully qualified names.
     * The method escapes special characters in the type name (e.g., ".", "$", "[", "]") and constructs a pattern
     * that matches either the fully qualified name or the simple name of the type.
     *
     * <p>For example:
     * <ul>
     *   <li>For a simple name like "List", the pattern will match both "List" and "java.util.List".</li>
     *   <li>For a fully qualified name like "java.util.List", the pattern will match both "java.util.List" and "List".</li>
     *   <li>For the wildcard "*", the pattern will match the literal "*".</li>
     * </ul>
     *
     * @param type the type name to create a pattern for. Must not be null, but can be empty or contain special characters.
     * @return a regex pattern string that matches the given type name, considering both simple and fully qualified forms.
     * @throws NullPointerException if the input type is null.
     */
    public static String createSimpleTypePattern(String type) {
        // TODO: implement this method
    }
}