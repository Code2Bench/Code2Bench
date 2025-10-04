package p150;

import java.util.*;

public class Tested {
    /**
     * Separates a full method signature into its class name and method signature components.
     * The method expects a full signature in the format "ClassName.methodName(parameters)".
     * It identifies the last '.' before the opening parenthesis '(' to split the string.
     *
     * @param fullSig The full method signature to be separated. Must not be null.
     * @return A String array of length 2 where the first element is the class name and the second
     *         element is the method signature (including parameters). Returns null if the input
     *         does not contain a valid method signature format (i.e., no '(' or no '.' before '(').
     * @throws NullPointerException if {@code fullSig} is null.
     */
    public static String[] sepClassAndMthSig(String fullSig) {
        if (fullSig == null) {
            throw new NullPointerException("fullSig cannot be null");
        }

        int lastDot = fullSig.lastIndexOf('.');
        if (lastDot == -1 || fullSig.charAt(lastDot + 1) != '(') {
            return null;
        }

        int lastParen = fullSig.lastIndexOf('(');
        if (lastParen == -1 || lastParen < lastDot || lastParen > lastDot + 1) {
            return null;
        }

        String className = fullSig.substring(0, lastDot);
        String methodSig = fullSig.substring(lastDot + 1, lastParen);

        return new String[]{className, methodSig};
    }
}