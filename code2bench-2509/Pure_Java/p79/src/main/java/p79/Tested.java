package p79;

import java.util.Arrays;

public class Tested {
    /**
     * Calculates a clamped analog position based on the given coordinates and directional inputs.
     * The method ensures that the resulting position does not exceed a maximum distance from the
     * original position (x, y). The directional inputs (lx, ly) are scaled by 30F to determine
     * the displacement. If the squared distance of the displacement exceeds the maximum allowed
     * squared distance (30F * 30F), the displacement is scaled down proportionally to ensure it
     * remains within the limit.
     *
     * @param x The x-coordinate of the original position.
     * @param y The y-coordinate of the original position.
     * @param lx The x-component of the directional input, typically in the range [-1, 1].
     * @param ly The y-component of the directional input, typically in the range [-1, 1].
     * @return A float array containing the clamped position as [newX, newY], where newX = x + dx
     *         and newY = y + dy, with dx and dy being the clamped displacement values.
     */
    public static float[] getClampedAnalogPosition(float x, float y, float lx, float ly) {
        // Calculate the displacement based on directional inputs
        float dx = lx * 30f;
        float dy = ly * 30f;
        
        // Calculate the squared distance of the displacement
        float squaredDistance = dx * dx + dy * dy;
        
        // Maximum allowed squared distance
        float maxSquaredDistance = 30f * 30f;
        
        // If the squared distance exceeds the maximum, scale down the displacement
        if (squaredDistance > maxSquaredDistance) {
            float scaleFactor = maxSquaredDistance / squaredDistance;
            dx = dx * scaleFactor;
            dy = dy * scaleFactor;
        }
        
        // Clamp the displacement to ensure it doesn't exceed the maximum distance
        float maxDistance = (float) Math.sqrt(maxSquaredDistance);
        if (Math.hypot(dx, dy) > maxDistance) {
            float scaleFactor = maxDistance / Math.hypot(dx, dy);
            dx = dx * scaleFactor;
            dy = dy * scaleFactor;
        }
        
        // Return the clamped position
        return new float[]{x + dx, y + dy};
    }
}