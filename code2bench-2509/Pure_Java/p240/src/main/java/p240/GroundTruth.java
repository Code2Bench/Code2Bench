package p240;
public class GroundTruth {
    public static boolean isSecuredNetwork(String capabilities) {
        if (capabilities == null || capabilities.isEmpty()) {
            return true; // Default to secured for safety
        }
        
        String caps = capabilities.toUpperCase();
        
        // Check for open network indicators
        if (caps.contains("[ESS]") && !caps.contains("WPA") && 
            !caps.contains("WEP") && !caps.contains("PSK") && 
            !caps.contains("EAP")) {
            return false; // Open network
        }
        
        // Check for security protocols
        return caps.contains("WPA") || caps.contains("WEP") || 
               caps.contains("PSK") || caps.contains("EAP") ||
               caps.contains("SAE") || caps.contains("OWE");
    }
}