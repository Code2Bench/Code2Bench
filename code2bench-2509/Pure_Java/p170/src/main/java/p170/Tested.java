public class Tested {
    /**
     * Extracts the UTF-8 encoded length and the updated offset from a byte array starting at the specified offset.
     * The method first skips the UTF-16 length of the string if present, then reads the UTF-8 encoded length.
     * The UTF-16 length is determined by checking the most significant bit of the first byte at the offset.
     * The UTF-8 length is read similarly, with support for multi-byte lengths if the most significant bit is set.
     *
     * @param array The byte array from which to extract the UTF-8 length and offset. Must not be null and must have
     *              sufficient length to read the required bytes starting at the specified offset.
     * @param offset The starting position in the byte array to begin reading. Must be a valid index within the array.
     * @return An int array of length 2, where the first element is the updated offset after reading the UTF-8 length,
     *         and the second element is the UTF-8 encoded length of the string.
     * @throws ArrayIndexOutOfBoundsException if the offset is invalid or the array does not contain sufficient bytes
     *         to read the UTF-16 or UTF-8 length.
     */
    public static int[] getUtf8(byte[] array, int offset) {
        // Check if the array is null or the offset is invalid
        if (array == null || offset < 0) {
            throw new ArrayIndexOutOfBoundsException("Invalid input: array or offset is invalid");
        }

        // Skip UTF-16 length if present
        int utf16Length = 0;
        if (offset + 1 < array.length) {
            byte firstByte = array[offset];
            if ((firstByte & 0x80) == 0) {
                // Single byte UTF-16
                utf16Length = firstByte & 0x0F;
            } else {
                // Multi-byte UTF-16
                utf16Length = (firstByte & 0xC0) << 8 | (array[offset + 1] & 0x3F);
            }
            offset += 2;
        }

        // Read UTF-8 length
        int utf8Length = 0;
        if (offset + 1 < array.length) {
            byte firstByte = array[offset];
            if ((firstByte & 0x80) == 0) {
                // Single byte UTF-8
                utf8Length = firstByte & 0x7F;
            } else {
                // Multi-byte UTF-8
                int length = 0;
                int i = offset + 1;
                while ((array[i] & 0x80) != 0) {
                    length = (length << 7) | (array[i] & 0x7F);
                    i++;
                }
                utf8Length = length;
                offset = i;
            }
        }

        return new int[]{offset, utf8Length};
    }
}