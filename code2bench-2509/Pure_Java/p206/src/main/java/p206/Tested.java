package p206;

import java.util.*;

public class Tested {
    /**
     * Transforms the metadata of a pillar based on the coordinate base mode. The method performs
     * the following operations:
     * <ul>
     *   <li>If the coordinate base mode is 0 or 2, the metadata is returned unchanged.</li>
     *   <li>Otherwise, the metadata is decomposed into type (lower 2 bits) and rotation (bits 2-3).</li>
     *   <li>If the rotation is 4, it is swapped with 8, and the result is combined with the type.</li>
     *   <li>If the rotation is 8, it is swapped with 4, and the result is combined with the type.</li>
     *   <li>If the rotation is neither 4 nor 8, the metadata is returned unchanged.</li>
     * </ul>
     *
     * @param meta The metadata of the pillar, where the lower 2 bits represent the type and bits 2-3 represent the rotation.
     * @param coordBaseMode The coordinate base mode, which determines how the metadata is transformed.
     * @return The transformed metadata based on the coordinate base mode and the original metadata.
     */
    public static int transformMetaPillar(int meta, int coordBaseMode) {
        if (coordBaseMode == 0 || coordBaseMode == 2) {
            return meta;
        }

        int type = meta & 0b11; // Extract lower 2 bits for type
        int rotation = (meta >> 2) & 0b11; // Extract bits 2-3 for rotation

        if (rotation == 4) {
            int temp = type;
            type = rotation;
            rotation = temp;
        } else if (rotation == 8) {
            int temp = type;
            type = rotation;
            rotation = temp;
        }

        return (type << 4) | rotation;
    }
}