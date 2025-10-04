package p3;

import java.util.Objects;

public class Tested {
    /**
     * Converts the given object to a string representation. If the object is null, the specified
     * default value is returned. If the object is already a string, it is returned as is. Otherwise,
     * the object's {@code toString()} method is invoked to obtain its string representation.
     * 
     * Note: This method is not yet implemented.
     *
     * @param value the object to convert to a string, may be null
     * @param defaultValue the string to return if the object is null, must not be null
     * @return the string representation of the object, or the default value if the object is null
     * @throws NullPointerException if the {@code defaultValue} is null (potential behavior, not confirmed)
     */
    public static String toStr(Object value, String defaultValue) {
        if (value == null) {
            return defaultValue;
        }
        return value.toString();
    }
}