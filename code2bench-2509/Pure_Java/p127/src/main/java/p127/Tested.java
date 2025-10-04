package p127;

import java.util.Objects;

public class Tested {
    /**
     * Calculates the frame size based on the provided byte array and size.
     * The method interprets the byte array as a little-endian integer and returns
     * the corresponding frame size. The size parameter determines how many bytes
     * from the array are used to calculate the frame size.
     *
     * <p>If the size is 2, the method interprets the first two bytes as a 16-bit
     * integer. If the size is 4, the method interprets the first four bytes as a
     * 32-bit integer. For any other size, the method returns -1.
     *
     * @param bytes The byte array containing the frame size data. Must not be null.
     * @param size The number of bytes to use for the frame size calculation. Must be either 2 or 4.
     * @return The calculated frame size as an integer. Returns -1 if the size is neither 2 nor 4.
     * @throws NullPointerException if the bytes array is null.
     */
    public static int getFrameSize(byte[] bytes, int size) {
        if (bytes == null) {
            throw new NullPointerException("bytes array cannot be null");
        }

        if (size != 2 && size != 4) {
            return -1;
        }

        int offset = 0;
        if (size == 2) {
            offset = 0;
        } else {
            offset = 0;
        }

        try {
            return (int) (bytes[offset] << 24) | (bytes[offset + 1] << 16) | (bytes[offset + 2] << 8) | bytes[offset + 3];
        } catch (Exception e) {
            return -1;
        }
    }
}