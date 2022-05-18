import org.junit.*;
import oop.ex3.searchengine.*;

import static org.junit.Assert.*;

public class BoopingSiteTest {
    private static final String FIRST_FILE = "hotels_tst1.txt";
    private static final String SECOND_FILE = "hotels_tst2.txt";


    private static final String FIRST_CITY = "manali";
    private static final String SECOND_CITY = "manafdli";

    private static final String RATING_ERROR_SORT = "the 2 objects are not sorted correctly through rating " +
            "(the array isn't sorted correctly)!";

    private static final String DISTANCE_ERROR_SORT = "the 2 objects are not sorted correctly through " +
            "rating (the array isn't sorted correctly)!";

    private static final double LONGITUDE = 0.0;
    private static final double LATITUDE  = 0.0;
    private static final int ZERO_APPEARANCE = 0;


    /**
     * this function checks the function getHotelsInCityByRating
     */
    @Test
    public void TestGetHotelsInCityByRating(){
        //text actual data
        BoopingSite b = new BoopingSite(FIRST_FILE);
        Hotel[] hotels = b.getHotelsInCityByRating(FIRST_CITY);
        for(int i = 0; i < hotels.length - 1; i++){
            Hotel hotel1 = hotels[i];
            Hotel hotel2 = hotels[i+1];
            if(hotel1.getStarRating() != hotel2.getStarRating()){
                assertTrue(RATING_ERROR_SORT, hotel1.getStarRating() > hotel2.getStarRating());
            }else{
                assertTrue(RATING_ERROR_SORT,
                        hotel1.getPropertyName().compareTo(hotel2.getPropertyName()) <= 0);
            }
        }
        //no real city. i.e. should return an empty array
        assertEquals(RATING_ERROR_SORT, ZERO_APPEARANCE, b.getHotelsInCityByRating(SECOND_CITY).length);
    }

    /**
     * this function checks the function getHotelsByProximity
     */
    @Test
    public void TestGetHotelsByProximity(){
        //text actual data
        BoopingSite b = new BoopingSite(FIRST_FILE);
        Hotel[] hotels = b.getHotelsByProximity(LATITUDE , LONGITUDE);
        for(int i = 0; i < hotels.length - 1; i++){
            Hotel hotel1 = hotels[i];
            Hotel hotel2 = hotels[i+1];
            if(Distance(hotel1, LATITUDE, LONGITUDE) != Distance(hotel2, LATITUDE, LONGITUDE)){
                assertTrue(DISTANCE_ERROR_SORT, Distance(hotel1, LATITUDE, LONGITUDE)
                        < Distance(hotel2, LATITUDE, LONGITUDE));
            }else{
                assertTrue(DISTANCE_ERROR_SORT, hotel1.getNumPOI() >= hotel2.getNumPOI());
            }
        }
    }

    /**
     * this function checks the function getHotelsInCityByProximity
     */
    @Test
    public void TestGetHotelsInCityByProximity(){
        //text actual data
        BoopingSite b = new BoopingSite(FIRST_FILE);
        Hotel[] hotels = b.getHotelsInCityByProximity(FIRST_CITY, LATITUDE , LONGITUDE);
        for(int i = 0; i < hotels.length - 1; i++){
            Hotel hotel1 = hotels[i];
            Hotel hotel2 = hotels[i+1];
            if(Distance(hotel1, LATITUDE, LONGITUDE) != Distance(hotel2, LATITUDE, LONGITUDE)){
                assertTrue(DISTANCE_ERROR_SORT, Distance(hotel1, LATITUDE, LONGITUDE)
                        < Distance(hotel2, LATITUDE, LONGITUDE));
            }else{
                assertTrue(DISTANCE_ERROR_SORT, hotel1.getNumPOI() >= hotel2.getNumPOI());
            }
        }
        //no real city. i.e. should return an empty array
        assertEquals(RATING_ERROR_SORT, ZERO_APPEARANCE,
                b.getHotelsInCityByProximity(SECOND_CITY, LATITUDE , LONGITUDE).length);
    }

    /**
     *
     * @param hotel Hotel object
     * @param latitude double
     * @param longitude double
     * @return the distance between the hotel and the point
     */
    private double Distance(Hotel hotel, double latitude, double longitude){
        return Math.hypot(hotel.getLatitude() - latitude,hotel.getLongitude() - longitude);
    }
}
