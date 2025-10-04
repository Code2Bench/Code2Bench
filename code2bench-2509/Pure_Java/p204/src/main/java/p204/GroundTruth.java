package p204;
public class GroundTruth {
    public static double pointSegmentDist(int x1, int z1, int x2, int z2, int px, int pz) {
        int dx = x2 - x1;
        int dz = z2 - z1;

        // The segment is just a point
        if (dx == 0 && dz == 0) {
            // intellij is telling me that this is duplicated, but it would be more expensive to move it out of the if statements
            return Math.sqrt((px - x1) * (px - x1) + (pz - z1) * (pz - z1));
        }

        // Calculate the projection t of point P onto the infinite line through A and B
        double t = ((px - x1) * dx + (pz - z1) * dz) / (double) (dx * dx + dz * dz);

        // Closest to point (x1, z1)
        if (t < 0) {
            return Math.sqrt((px - x1) * (px - x1) + (pz - z1) * (pz - z1));
        } else if (t > 1) {
            // Closest to point (x2, z2)
            return Math.sqrt((px - x2) * (px - x2) + (pz - z2) * (pz - z2));
        }
        // Projection is within the segment

        double projX = x1 + t * dx;
        double projZ = z1 + t * dz;

        // Magic math
        return Math.sqrt((px - projX) * (px - projX) + (pz - projZ) * (pz - projZ));
    }
}