package p105;

import java.util.Objects;

public class Tested {
    /**
     * Converts the given object to a {@code Double} value. The method handles the following cases:
     * <ul>
     *   <li>If the object is already a {@code Double}, it is returned directly.</li>
     *   <li>If the object is a {@code Float}, it is converted to a {@code Double} using {@link Float#doubleValue()}.</li>
     *   <li>For all other types, the object is converted to a string using {@link Object#toString()} and then parsed as a {@code Double}.</li>
     * </ul>
     *
     * @param o the object to convert to a {@code Double}. Must not be {@code null}.
     * @return the {@code Double} value corresponding to the input object.
     * @throws NullPointerException if the input object is {@code null}.
     * @throws NumberFormatException if the object's string representation cannot be parsed as a {@code Double}.
     */
    public static Double convertToDouble(Object o) {
        if (o == null) {
            throw new NullPointerException("Input object cannot be null");
        }

        if (o instanceof Double) {
            return (Double) o;
        } else if (o instanceof Float) {
            return Double.valueOf(o.toString());
        } else {
            try {
                return Double.parseDouble(o.toString());
            } catch (NumberFormatException e) {
                throw new NumberFormatException("Cannot parse object to Double: " + o);
            }
        }
    }
}