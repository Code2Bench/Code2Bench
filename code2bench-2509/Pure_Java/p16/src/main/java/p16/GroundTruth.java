package p16;
public class GroundTruth {
    public static String stripTrailingSemicolon(String sql) {
        int i = sql.length()-1;
        while (i>=0 && Character.isWhitespace(sql.charAt(i))) i--;
        if (i>=0 && sql.charAt(i)==';') return sql.substring(0, i);
        return sql;
    }
}