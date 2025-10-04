package p14;

import java.util.Objects;

public class Tested {
    /**
     * Escapes a field for use in a CSV format. If the field contains commas, double quotes, or newlines,
     * it will be enclosed in double quotes, and any existing double quotes will be escaped by doubling them.
     * If the field is {@code null}, an empty string is returned.
     *
     * @param field The field to be escaped. Can be {@code null}.
     * @return The escaped field as a {@code String}. If the field is {@code null}, an empty string is returned.
     */
    private static String escapeCsvField(Object field) {
        if (field == null) {
            return "";
        }

        StringBuilder sb = new StringBuilder();
        String value = field.toString();

        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (c == '"') {
                sb.append("'");
                sb.append(c);
            } else if (c == ',') {
                sb.append(",");
                sb.append('"');
            } else if (c == '\n') {
                sb.append("\n");
                sb.append('"');
            } else {
                sb.append(c);
            }
        }

        return sb.toString();
    }
}