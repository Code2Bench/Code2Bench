package p168;
public class GroundTruth {
    public static String makeLinkHtml(String plain) {
        if (plain == null || plain.isEmpty()) {
            return "";
        }
        String encodedPlain = plain.replace("&", "&amp;");
        return "<a href=\"" + encodedPlain + "\">" + encodedPlain + "</a>";
    }
}