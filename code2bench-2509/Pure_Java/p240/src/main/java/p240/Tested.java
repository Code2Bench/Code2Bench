public class Tested {
    /**
     * Determines if a network is secured based on its capabilities string.
     *
     * <p>The method checks for the presence of security protocols such as WPA, WEP, PSK, EAP, SAE, or OWE
     * in the provided capabilities string. If none of these protocols are found and the string contains
     * "[ESS]" (indicating an open network), the network is considered unsecured. If the capabilities
     * string is null or empty, the method defaults to considering the network as secured for safety.
     *
     * @param capabilities the network capabilities string to evaluate. Can be null or empty.
     * @return {@code true} if the network is secured (either due to the presence of security protocols
     *         or because the capabilities string is null/empty), {@code false} if the network is open.
     */
    public static boolean isSecuredNetwork(String capabilities) {
        if (capabilities == null || capabilities.isEmpty()) {
            return true;
        }

        // Check for security protocols
        String[] protocols = {"WPA", "WEP", "PSK", "EAP", "SAE", "OWE"};
        for (String protocol : protocols) {
            if (capabilities.contains(protocol)) {
                return true;
            }
        }

        // Check for open network (ESS)
        if (capabilities.contains("[ESS]")) {
            return false;
        }

        // If none of the above, consider it as secured
        return true;
    }
}