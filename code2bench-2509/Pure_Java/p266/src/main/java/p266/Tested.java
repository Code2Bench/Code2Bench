package p266;

import java.util.Objects;

public class Tested {
    /**
     * Searches for the first occurrence of a specified name preceded by a forward slash ('/') in a byte array.
     * The method iterates through the byte array, looking for a '/' character. When found, it checks if the
     * subsequent bytes match the characters of the provided name. If a match is found, the index of the '/'
     * character is returned. If no match is found, the method returns -1.
     *
     * @param d The byte array to search within. Must not be null.
     * @param name The name to search for after a '/'. Must not be null.
     * @return The index of the '/' character preceding the matched name, or -1 if no match is found.
     * @throws NullPointerException if either {@code d} or {@code name} is null.
     */
    private static int findSlashName(byte[] d, String name) {
        if (d == null || name == null) {
            throw new NullPointerException("d and name cannot be null");
        }

        for (int i = 0; i < d.length; i++) {
            if (d[i] == '/') {
                // Check if the next characters match the name
                if (i + name.length() <= d.length) {
                    for (int j = 0; j < name.length(); j++) {
                        if (d[i + j] != name.charAt(j)) {
                            break;
                        }
                    }
                    if (j == name.length()) {
                        return i;
                    }
                }
            }
        }
        return -1;
    }
}