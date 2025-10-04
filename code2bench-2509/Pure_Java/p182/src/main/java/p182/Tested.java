public class Tested {
    /**
     * Calculates the index of a given note within a specified set of intervals, relative to a tonic.
     * The method computes the relative position of the note with respect to the tonic, and then
     * searches for this relative position within the intervals array. If found, the index of the
     * interval is returned; otherwise, the method returns 0.
     *
     * @param intervals An array of integers representing the intervals to search within. Must not be null.
     * @param note The note whose index is to be calculated. This is an absolute value, typically a MIDI note number.
     * @param tonic The tonic note, represented as an integer where 0 corresponds to C, 1 to C#, ..., 11 to B.
     * @return The index of the interval that matches the relative note position, or 0 if no match is found.
     * @throws NullPointerException if the intervals array is null.
     */
    public static int calcNoteIndex(final int[] intervals, final int note, final int tonic) {
        if (intervals == null) {
            throw new NullPointerException("intervals cannot be null");
        }

        // Calculate the relative position of the note with respect to the tonic
        int relativeNote = note - tonic;

        // Find the index of the relativeNote in the intervals array
        return Arrays.binarySearch(intervals, relativeNote);
    }
}