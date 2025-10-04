package p145;

public class Tested {
    /**
     * Removes the specified prefix from the beginning of the given string if it starts with that prefix.
     * If the string does not start with the prefix, the original string is returned unchanged.
     *
     * @param str The string from which the prefix should be removed. Must not be null.
     * @param prefix The prefix to remove from the string. Must not be null.
     * @return The string with the prefix removed if it started with the prefix; otherwise, the original string.
     * @throws NullPointerException if either {@code str} or {@code prefix} is null.
     */
    public static String removePrefix(String str, String prefix) {
        if (str == null || prefix == null) {
            throw new NullPointerException("str or prefix cannot be null");
        }
        
        int prefixLength = prefix.length();
        if (prefixLength == 0) {
            return str;
        }
        
        int strLength = str.length();
        if (strLength < prefixLength) {
            return str;
        }
        
        return str.substring(prefixLength);
    }
}