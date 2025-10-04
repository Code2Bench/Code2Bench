package p2;

public class Tested {
    /**
     * Extracts and returns the file type (extension) from the given file name. The file type is
     * determined by the substring after the last occurrence of the '.' character in the file name.
     * If the file name does not contain a '.', an empty string is returned.
     *
     * @param fileName the file name from which to extract the file type.
     * @return the file type, or an empty string if the file name does not contain a '.'.
     */
    public static String getFileType(String fileName) {
        if (fileName == null || fileName.isEmpty()) {
            return "";
        }
        
        int lastDotIndex = fileName.lastIndexOf('.');
        if (lastDotIndex == -1) {
            return "";
        }
        
        return fileName.substring(lastDotIndex + 1);
    }
}