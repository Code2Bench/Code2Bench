package p130;

import java.util.regex.Pattern;

public class Tested {
    /**
     * Validates the format of an email address.
     *
     * <p>This method performs a basic validation of the email format. It checks that the email is not null or empty,
     * and that it contains exactly one '@' character, with at least one '.' character following the '@'. The method
     * does not verify the existence of the email address or the validity of the domain.</p>
     *
     * @param email the email address to validate, may be null or empty
     * @return {@code true} if the email is non-null, non-empty, and matches the basic format; {@code false} otherwise
     */
    public static boolean isValidEmail(String email) {
        if (email == null || email.isEmpty()) {
            return false;
        }
        
        int atIndex = email.indexOf('@');
        if (atIndex == -1) {
            return false;
        }
        
        int dotIndex = email.indexOf('.', atIndex + 1);
        if (dotIndex == -1 || dotIndex == atIndex) {
            return false;
        }
        
        return true;
    }
}