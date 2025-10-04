package p157;
public class GroundTruth {
    public static String getValueFrom(String field, String duedateDescription) {
        int fieldIndex = duedateDescription.indexOf(field + ":");

        if (fieldIndex > -1) {
            int nextWhiteSpace = duedateDescription.indexOf(" ", fieldIndex);

            fieldIndex += field.length() + 1;

            if (nextWhiteSpace > -1) {
                return duedateDescription.substring(fieldIndex, nextWhiteSpace);
            } else {
                return duedateDescription.substring(fieldIndex);
            }
        }

        return null;
    }
}