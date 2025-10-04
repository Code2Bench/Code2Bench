package p125;
public class GroundTruth {
    public static int getCellCoordinate(
            Integer currentCoordinate, Integer absoluteCoordinate, Integer relativeCoordinate) {
        if (absoluteCoordinate != null && absoluteCoordinate > 0) {
            return absoluteCoordinate;
        }
        if (relativeCoordinate != null) {
            return currentCoordinate + relativeCoordinate;
        }
        return currentCoordinate;
    }
}