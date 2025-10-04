package p40;

/**
 * Compares two strings, treating {@code null} values as less than non-null values.
 * If both strings are {@code null}, they are considered equal. If one of the strings
 * is {@code null}, it is considered less than the non-null string. If neither
 * string is {@code null}, they are compared lexicographically using {@link String#compareTo}.
 *
 * @param s1 the first string to compare, may be {@code null}
 * @param s2 the second string to compare, may be {@code null}
 * @return a negative integer, zero, or a positive integer as the first string is
 *         less than, equal to, or greater than the second string, respectively.
 *         Specifically:
 *         <ul>
 *           <li>0 if both strings are {@code null}</li>
 *           <li>1 if the first string is {@code null} and the second is not</li>
 *           <li>-1 if the second string is {@code null} and the first is not</li>
 *           <li>the result of {@code s1.compareTo(s2)} if neither string is {@code null}</li>
 *         </ul>
 */
public class Tested {
    public static int compareNullLast(String s1, String s2) {
        if (s1 == null) {
            if (s2 == null) {
                return 0;
            }
            return 1;
        }
        if (s2 == null) {
            return -1;
        }
        return s1.compareTo(s2);
    }
}