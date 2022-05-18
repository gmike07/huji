import oop.ex2.*;
/**
 * This class represents a space ship factory, has methods to produce ship arrays from string arrays, via
 * the createSpaceShips function
 */
public class SpaceShipFactory {

    /* this constant hold the string representing a human ship */
    private static final String HUMAN = "h";

    /* this constant hold the string representing a runner ship */
    private static final String RUNNER = "r";

    /* this constant hold the string representing a basher ship */
    private static final String BASHER = "b";

    /* this constant hold the string representing an aggressive ship */
    private static final String AGRESSIVE = "a";

    /* this constant hold the string representing a drunkard ship */
    private static final String DRUNKARD = "d";

    /* this constant hold the string representing a special ship */
    private static final String SPECIAL = "s";

    /**
     * @param args gets a string array, string[i] represents a ship type
     * @return a spaceship array, spaceship[i] is an object of the type represented in string[i]
     */
    public static SpaceShip[] createSpaceShips(String[] args) {
        SpaceShip[] spaceships = new SpaceShip[args.length];
        for(int i = 0; i < spaceships.length; i++)
            spaceships[i] = createSpaceShip(args[i]);
        return spaceships;
    }

    /**
     * @param arg gets a string representing a type of ship
     * @return return a space ship that the arg represented
     */
    private static SpaceShip createSpaceShip(String arg){
        if (arg.equals(HUMAN))
            return new HumanSpaceShip();
        if (arg.equals(RUNNER))
            return new RunnerSpaceShip();
        if (arg.equals(BASHER))
            return new BasherSpaceShip();
        if (arg.equals(AGRESSIVE))
            return new AggressiveSpaceShip();
        if (arg.equals(DRUNKARD))
            return new DrunkardSpaceShip();
        if (arg.equals(SPECIAL))
            return new SpecialSpaceShip();
        return null;
    }
}
