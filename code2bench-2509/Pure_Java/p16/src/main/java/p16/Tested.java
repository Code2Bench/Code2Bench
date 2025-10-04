package p16;

public class Tested {
    public static String stripTrailingSemicolon(String sql) {
        // Trim trailing whitespace
        String trimmed = sql.trim();
        
        // Check if the last character is a semicolon
        if (trimmed.length() > 0 && trimmed.charAt(trimmed.length() - 1) == ';') {
            return trimmed.substring(0, trimmed.length() - 1);
        }
        
        return sql;
    }
}