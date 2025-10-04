package p198;
public class GroundTruth {
    public static float[] parseFloatArray(String s){
        if(s.isEmpty()){
            return new float[0];
        }
        String[] numbers = s.split(" ");
        float[] arr = new float[numbers.length];
        for(int i = 0; i < numbers.length; i ++){
            arr[i] = Float.parseFloat(numbers[i]);
        }
        return arr;
    }
}