package p180;

public class Tested {
    /**
     * Filters the input string by replacing specific characters with their corresponding HTML/XML entities.
     * The method handles the following character replacements:
     * <ul>
     *   <li>'<' → "&lt;"</li>
     *   <li>'>' → "&gt;"</li>
     *   <li>'"' → "&quot;"</li>
     *   <li>'\'' → "&#39;"</li>
     *   <li>'%' → "&#37;"</li>
     *   <li>';' → "&#59;"</li>
     *   <li>'(' → "&#40;"</li>
     *   <li>')' → "&#41;"</li>
     *   <li>'&' → "&amp;"</li>
     *   <li>'+' → "&#43;"</li>
     * </ul>
     * If the input string is {@code null}, the method returns {@code null}.
     *
     * @param value the input string to filter, may be {@code null}
     * @return the filtered string with special characters replaced by their HTML/XML entities, or {@code null} if the input is {@code null}
     */
    public static String filter(String value) {
        // TODO: implement this method
    }
}