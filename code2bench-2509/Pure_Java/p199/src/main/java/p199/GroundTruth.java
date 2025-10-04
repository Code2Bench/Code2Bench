package p199;
public class GroundTruth {
    public static int[] parseIntegerArray(String s){
        String[] numbers = s.split(" ");
        int[] arr = new int[numbers.length];
        for(int i = 0; i < numbers.length; i ++){
            arr[i] = Integer.parseInt(numbers[i]);
        }
        return arr;
    }
}