package p204;

import java.lang.Math;

public class Tested {
    /**
     * Calculates the shortest distance between a point and a line segment defined by two endpoints.
     * The method computes the Euclidean distance from the point to the closest point on the segment.
     *
     * <p>If the segment is degenerate (i.e., both endpoints are the same), the distance is computed
     * directly between the point and the single endpoint. Otherwise, the method calculates the projection
     * of the point onto the infinite line through the endpoints and determines the closest point on the
     * segment by clamping the projection parameter {@code t} to the range [0, 1].
     *
     * @param x1 The x-coordinate of the first endpoint of the segment.
     * @param z1 The z-coordinate of the first endpoint of the segment.
     * @param x2 The x-coordinate of the second endpoint of the segment.
     * @param z2 The z-coordinate of the second endpoint of the segment.
     * @param px The x-coordinate of the point.
     * @param pz The z-coordinate of the point.
     * @return The shortest distance between the point and the segment, as a double.
     */
    public static double pointSegmentDist(int x1, int z1, int x2, int z2, int px, int pz) {
        // Check if the segment is degenerate (both endpoints are the same)
        if (x1 == x2 && z1 == z2) {
            return Math.hypot(px - x1, pz - z1);
        }

        // Define vectors for the line segment
        int dx = x2 - x1;
        int dz = z2 - z1;
        
        // Vector from point to first endpoint
        int dxp = px - x1;
        int dzp = pz - z1;
        
        // Compute the dot product of vector AP and vector AB
        double dotProduct = dxp * dx + dzp * dz;
        
        // Compute the square of the length of vector AB
        double abLengthSq = dx * dx + dz * dz;
        
        // Compute the parameter t for the projection
        double t = dotProduct / abLengthSq;
        
        // Clamp t to the range [0, 1]
        double tClamped = Math.max(0.0, Math.min(1.0, t));
        
        // Compute the closest point on the segment
        int x = x1 + (int) (dx * tClamped);
        int z = z1 + (int) (dz * tClamped);
        
        // Compute the distance from the point to the closest point on the segment
        double distance = Math.hypot(px - x, pz - z);
        
        return distance;
    }
}