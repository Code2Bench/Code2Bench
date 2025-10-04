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
        // TODO: implement this method
    }
}