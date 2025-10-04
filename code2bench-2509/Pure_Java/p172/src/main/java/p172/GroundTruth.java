package p172;
public class GroundTruth {
    public static int indexOfSpecial(String message, int pos) {
        for ( int i = pos; i < message.length(); i++ )
        {
            char c = message.charAt( i );

            if ( c == ' ' || Character.isISOControl( c ) )
            {
                return i;
            }
        }
        return -1;
    }
}