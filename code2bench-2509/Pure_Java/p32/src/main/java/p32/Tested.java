public class Tested {
    /**
     * Converts a given class name into an instance variable name by converting the first character to lowercase,
     * appending the remaining substring, and adding the suffix "Strategy". If the input class name is null or empty,
     * the method returns the input as is.
     *
     * <p>For example, {@code toInstanceVariableName("MyClass")} returns {@code "myClassStrategy"}.</p>
     *
     * @param className the class name to convert, may be null or empty
     * @return the converted instance variable name, or the input if it is null or empty
     */
    public static String toInstanceVariableName(String className) {
        if (className == null || className.isEmpty()) {
            return className;
        }
        
        // Convert first character to lowercase
        char firstChar = className.charAt(0);
        StringBuilder sb = new StringBuilder();
        sb.append(Character.toLowerCase(firstChar));
        
        // Append the remaining substring
        sb.append(className.substring(1));
        
        // Add the suffix "Strategy"
        sb.append("Strategy");
        
        return sb.toString();
    }
}