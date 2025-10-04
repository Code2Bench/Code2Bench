package p257;

import java.nio.ByteOrder;

public class Tested {
    /**
     * Reads a multi-byte number from a byte array starting at a specified position.
     * The number is constructed by interpreting the specified number of bytes as a big-endian integer.
     * Each byte is masked with 0xff to ensure it is treated as an unsigned value.
     *
     * @param sbuf The byte array from which to read the number. Must not be null.
     * @param pos The starting position in the byte array. Must be a valid index within the bounds of the array.
     * @param numBytes The number of bytes to read. Must be a positive integer and not exceed the remaining bytes in the array starting from the specified position.
     * @return The integer value constructed from the specified bytes.
     * @throws ArrayIndexOutOfBoundsException if {@code pos} is out of bounds or if {@code pos + numBytes} exceeds the length of {@code sbuf}.
     */
    private static int readNum(byte[] sbuf, int pos, int numBytes) {
        // Check if the input is valid
        if (sbuf == null || pos < 0 || numBytes <= 0) {
            throw new IllegalArgumentException("Invalid input parameters");
        }

        // Check if the position and number of bytes are within bounds
        if (pos + numBytes > sbuf.length) {
            throw new ArrayIndexOutOfBoundsException("Position and number of bytes exceed the length of the array");
        }

        // Initialize the result
        int result = 0;

        // Read each byte and mask it with 0xff
        for (int i = 0; i < numBytes; i++) {
            byte b = sbuf[pos + i];
            result = (result << 8) | (b & 0xFF);
        }

        return result;
    }
}