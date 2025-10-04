package p158;
public class GroundTruth {
    public static String removeValueFrom(String field, String duedateDescription) {
        int fieldIndex = duedateDescription.indexOf(field + ":");

        if (fieldIndex > -1) {
            int nextWhiteSpace = duedateDescription.indexOf(" ", fieldIndex);

            if (nextWhiteSpace > -1) {
                return duedateDescription.replace(duedateDescription.substring(fieldIndex, nextWhiteSpace), "");
            } else {
                return duedateDescription.substring(0, fieldIndex);
            }
        }

        return duedateDescription;
    }
}