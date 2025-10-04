package p166;
public class GroundTruth {
    public static String stripComments(String sql) {
        StringBuilder out = new StringBuilder(sql.length());
        boolean inS=false, inD=false, inLine=false, inBlock=false; // State flags
        for (int i=0;i<sql.length();i++){
            char c=sql.charAt(i), n=(i+1<sql.length()?sql.charAt(i+1):'\0');
            // Check for comment start/end if not inside a string literal
            if (!inS && !inD) {
                if (!inBlock && c=='-'&&n=='-'){inLine=true; i++; continue;}
                if (inLine && c=='\n'){inLine=false; continue;}
                if (!inLine && !inBlock && c=='/'&&n=='*'){inBlock=true; i++; continue;}
                if (inBlock && c=='*'&&n=='/'){inBlock=false; i++; continue;}
            }
            if (inLine || inBlock) continue; // Skip characters inside comments

            // Toggle string literal state
            if (!inD && c=='\''){inS=!inS; out.append(c); continue;}
            if (!inS && c=='"'){inD=!inD; out.append(c); continue;}
            out.append(c);
        }
        return out.toString();
    }
}