package p131;

import java.util.*;
import java.util.Map.Entry;

public class Helper {

    public static boolean deepCompare(Object a, Object b) {
        return deepCompare(a, b, 1e-6);
    }

    public static boolean deepCompare(Object a, Object b, double tolerance) {
        // Handle null cases
        if (a == null) {
            return b == null;
        }
        if (b == null) {
            return false;
        }

        // Compare numbers with tolerance
        if (a instanceof Number && b instanceof Number) {
            return Math.abs(((Number) a).doubleValue() - ((Number) b).doubleValue()) <= tolerance;
        }

        // Compare maps recursively
        if (a instanceof Map && b instanceof Map) {
            Map<?, ?> mapA = (Map<?, ?>) a;
            Map<?, ?> mapB = (Map<?, ?>) b;

            if (mapA.size() != mapB.size()) {
                return false;
            }

            for (Entry<?, ?> entry : mapA.entrySet()) {
                Object key = entry.getKey();
                if (!mapB.containsKey(key) || !deepCompare(entry.getValue(), mapB.get(key), tolerance)) {
                    return false;
                }
            }
            return true;
        }

        // Compare collections/lists recursively
        if (a instanceof Collection && b instanceof Collection) {
            Collection<?> colA = (Collection<?>) a;
            Collection<?> colB = (Collection<?>) b;

            if (colA.size() != colB.size()) {
                return false;
            }

            Iterator<?> iterA = colA.iterator();
            Iterator<?> iterB = colB.iterator();
            while (iterA.hasNext() && iterB.hasNext()) {
                if (!deepCompare(iterA.next(), iterB.next(), tolerance)) {
                    return false;
                }
            }
            return true;
        }

        // Compare arrays
        if (a.getClass().isArray() && b.getClass().isArray()) {
            int lengthA = java.lang.reflect.Array.getLength(a);
            int lengthB = java.lang.reflect.Array.getLength(b);

            if (lengthA != lengthB) {
                return false;
            }

            for (int i = 0; i < lengthA; i++) {
                if (!deepCompare(java.lang.reflect.Array.get(a, i),
                        java.lang.reflect.Array.get(b, i), tolerance)) {
                    return false;
                }
            }
            return true;
        }

        // Default comparison for other types
        return a.equals(b);
    }
}