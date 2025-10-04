package p187;
public class GroundTruth {
    public static double findOptimalYInterval(double max) {
        int base = 1;
        double [] divisions = new double [] {1,2,2.5,5};
        
        while (true) {
            
            for (int d=0;d<divisions.length;d++) {
                double tester = base * divisions[d];
                if (max / tester <= 10) {
                    return tester;
                }
            }
        
            base *=10;
            
        }
        
        
        
    }
}