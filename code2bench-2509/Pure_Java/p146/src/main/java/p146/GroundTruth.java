package p146;
public class GroundTruth {
    public static String fixType(String clsName) {
        switch (clsName.charAt(0)) {
            case '[':
                return clsName;

            case 'L':
            case 'T':
                if (clsName.endsWith(";")) {
                    return clsName;
                }
                break;
        }
        return 'L' + clsName + ';';
    }
}