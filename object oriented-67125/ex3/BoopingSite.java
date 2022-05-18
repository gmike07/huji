import oop.ex3.searchengine.*;
import java.util.Arrays;
import java.util.Comparator;

public class BoopingSite {
    /* has a list of all hotels in the file */
    private Hotel[] hotels;
    private static final int MAX_LATITUDE = 90;
    private static final int MAX_LONGTITUDE = 180;

    /**
     * @param name gets a name of a file
     */
    public BoopingSite(String name){
        hotels = HotelDataset.getHotels(name);
    }

    /**
     * @param city gets a string city
     * @return a sorted array by rating of the hotels in city
     */
    public Hotel[] getHotelsInCityByRating(String city){
        Hotel[] hotelsSorted = hotelsInCity(city);
        Arrays.sort(hotelsSorted, HotelsByRating());
        return hotelsSorted;
    }


    /**
     * @param city gets a string city
     * @return returns an array of only the hotels in that city
     */
    private Hotel[] hotelsInCity(String city) {
        int numInCity = 0;
        for(Hotel hotel: hotels)
            if(hotel.getCity().equals(city))
                numInCity++;
        Hotel[] hotelsSorted = new Hotel[numInCity];
        numInCity = 0;
        for(Hotel hotel: hotels)
            if(hotel.getCity().equals(city)) {
                hotelsSorted[numInCity] = hotel;
                numInCity++;
            }
        return hotelsSorted;
    }

    /**
     * @param latitude double
     * @param longitude double
     * @return a sorted array by distance of the hotels
     */
    public Hotel[] getHotelsByProximity(double latitude, double longitude){
        if(Math.abs(latitude) > MAX_LATITUDE || Math.abs(longitude) > MAX_LONGTITUDE)
            return new Hotel[0];
        Arrays.sort(hotels, HotelsByDistance(latitude, longitude));
        return hotels;
    }

    /**
     * @param city string that represents the city
     * @param latitude double
     * @param longitude double
     * @return a sorted array by distance of the hotels in city
     */
    public Hotel[] getHotelsInCityByProximity(String city, double latitude, double longitude){
        if(Math.abs(latitude) > MAX_LATITUDE || Math.abs(longitude) > MAX_LONGTITUDE)
            return new Hotel[0];
        Hotel[] hotelsSorted = hotelsInCity(city);
        Arrays.sort(hotelsSorted, HotelsByDistance(latitude, longitude));
        return hotelsSorted;
    }


    /**
     * @return a comparator for rating hotels
     */
    private Comparator<Hotel> HotelsByRating(){
        return new Comparator<Hotel>(){
            @Override
            public int compare(Hotel o1, Hotel o2){
                if(o1.getStarRating() != o2.getStarRating())
                    return o2.getStarRating() - o1.getStarRating();
                return o1.getPropertyName().compareTo(o2.getPropertyName());
            }
        };
    }

    /**
     *
     * @param latitude double
     * @param longitude double
     * @return a comparator for distance between hotels
     */
    private Comparator<Hotel> HotelsByDistance(double latitude, double longitude){
        return new Comparator<Hotel>(){
            @Override
            public int compare(Hotel o1, Hotel o2){
                double dist1 = Distance(o1, latitude, longitude);
                double dist2 = Distance(o2, latitude, longitude);
                if(dist1 != dist2)
                    return (int) Math.signum(dist1 - dist2);
                return o2.getNumPOI() - o1.getNumPOI();
            }
        };
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
