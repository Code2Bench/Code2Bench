package p47;

public class Tested {
    /**
     * Calculates the index path for a given crate name based on its length. The index path is constructed
     * as follows:
     * <ul>
     *   <li>If the crate name length is 1, the path is "1/{crateName}".</li>
     *   <li>If the crate name length is 2, the path is "2/{crateName}".</li>
     *   <li>If the crate name length is 3, the path is "3/{firstCharacter}/{crateName}".</li>
     *   <li>For crate names longer than 3 characters, the path is "{firstTwoCharacters}/{nextTwoCharacters}/{crateName}".</li>
     * </ul>
     *
     * @param crateName The name of the crate. Must not be null or empty.
     * @return The calculated index path as a String.
     * @throws IllegalArgumentException if the crate name is null or empty.
     */
    public static String calculateIndexPath(String crateName) {
        // TODO: implement this method
    }
}