package p272;

import java.util.Objects;

public class Tested {
    /**
     * Converts an array of CJK glyph codes into a byte array representing their encoding.
     * Each glyph code is split into two bytes: the high byte (bits 8-15) and the low byte (bits 0-7).
     * The resulting byte array has a length of {@code size * 2}, where each glyph is represented by two consecutive bytes.
     *
     * @param glyph An array of CJK glyph codes. Must not be null, and its length must be at least {@code size}.
     * @param size The number of glyphs to encode. Must be non-negative and less than or equal to the length of {@code glyph}.
     * @return A byte array containing the encoded glyphs. The length of the array is {@code size * 2}.
     * @throws NullPointerException if {@code glyph} is null.
     * @throws IllegalArgumentException if {@code size} is negative or greater than the length of {@code glyph}.
     */
    private static byte[] getCJKEncodingBytes(int[] glyph, int size) {
        if (glyph == null) {
            throw new NullPointerException("glyph cannot be null");
        }
        if (size < 0 || size > glyph.length) {
            throw new IllegalArgumentException("size must be non-negative and <= length of glyph");
        }

        byte[] result = new byte[size * 2];
        for (int i = 0; i < size; i++) {
            int glyphCode = glyph[i];
            // Split into high and low bytes
            int highByte = (glyphCode >> 8) & 0xFF;
            int lowByte = glyphCode & 0xFF;
            result[i * 2] = (byte) highByte;
            result[i * 2 + 1] = (byte) lowByte;
        }
        return result;
    }
}