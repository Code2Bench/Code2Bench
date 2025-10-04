package p137;

import java.util.*;

public class Tested {
    /**
     * Transforms the given name into a modified version based on specific rules.
     * <p>
     * The method applies the following transformations in sequence:
     * <ol>
     *   <li>If the name is null or empty, returns null.</li>
     *   <li>If the name consists entirely of uppercase characters, converts it to lowercase and returns the result.</li>
     *   <li>If the name does not already start with a lowercase letter, converts the first character to lowercase and returns the modified name.</li>
     *   <li>If the name is shorter than 3 characters, appends "Var" to the name and returns the result.</li>
     *   <li>If none of the above conditions are met, returns null.</li>
     * </ol>
     *
     * @param name The input name to be transformed. Can be null or empty.
     * @return The transformed name based on the rules above, or null if no transformation is applicable.
     */
    private static String fromName(String name) {
        if (name == null || name.isEmpty()) {
            return null;
        }
        
        // Check if all characters are uppercase
        boolean allUppercase = true;
        for (char c : name.toCharArray()) {
            if (!Character.isUpperCase(c)) {
                allUppercase = false;
                break;
            }
        }
        if (allUppercase) {
            return name.toLowerCase();
        }
        
        // Check if the name starts with a lowercase letter
        if (!name.startsWith(Character.toString(Character.toLowerCase(name.charAt(0))))) {
            return name.substring(0, 1).toLowerCase() + name;
        }
        
        // Check if the name is shorter than 3 characters
        if (name.length() < 3) {
            return name + "Var";
        }
        
        return null;
    }
}