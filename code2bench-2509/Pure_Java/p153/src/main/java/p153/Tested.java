package p153;

import java.util.Objects;

public class Tested {
    /**
     * Replaces all occurrences of each key in the input text with the corresponding value.
     * The replacement is performed sequentially for each key-value pair in the provided arrays.
     * If a key is found in the text, it is replaced with the corresponding value from the values array.
     *
     * @param text   The input text in which replacements are to be performed. Must not be null.
     * @param key    An array of strings representing the keys to be replaced. Must not be null, and its length must match the length of the values array.
     * @param values An array of strings representing the replacement values. Must not be null, and its length must match the length of the key array.
     * @return The modified text after all replacements have been performed. Returns the original text if no replacements are made.
     * @throws NullPointerException if any of the parameters (text, key, or values) are null.
     * @throws IllegalArgumentException if the lengths of the key and values arrays do not match.
     */
    private static String stringUtils(String text, String[] key, String[] values) {
        if (text == null || key == null || values == null) {
            throw new NullPointerException("text, key, or values cannot be null");
        }
        
        if (key.length != values.length) {
            throw new IllegalArgumentException("Key and values arrays must have the same length");
        }

        StringBuilder result = new StringBuilder(text);
        for (int i = 0; i < key.length; i++) {
            String keyStr = key[i];
            String valueStr = values[i];
            
            // Check if key is present in the text
            if (result.toString().contains(keyStr)) {
                // Replace the first occurrence of the key
                int index = result.toString().indexOf(keyStr);
                result.replace(index, index + keyStr.length(), valueStr);
            }
        }
        
        return result.toString();
    }
}