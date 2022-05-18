import java.util.Random;
/**
 * This class represents a drunkard space ship, which extends the class SpaceShip and overrides the
 * doAction function
 */
public class DrunkardSpaceShip extends SpaceShip {

    /* this constant holds the constant to roll a number between -1,0,1 */
    private static final int TURNING_CHANCE = 2;

    /* this constant holds the chance of the drunkard to shoot */
    private static final int SHOOTING_CHANCE = 63;

    /* this constant holds the chance of the drunkard to teleport */
    private static final int TELEPORTING_CHANCE = 1023;

    /* this constant holds the chance of the drunkard to shield */
    private static final int SHIELDING_CHANCE = 5;

    /* this constant holds the min amount of movement the drunkard is allowed to do in one frame */
    private static final int TURN_MIN = 1;

    /* this constant holds the max amount of movement the drunkard is allowed to do in one frame */
    private static final int TURN_MAX = 5;

    /* this constant holds the minimum distance to allow the space ship to bash */
    private static final double BASHING_DISTANCE = 0.19;

    /* this variable hold the last choice to which turn did the drunkard do */
    private int lastTurnChoice = 1;
    /* this object handles the randomness of the drunkard */
    private Random random;

    /**
     * This constructor builds a new "Drunkard" space ship as requested by the exercise
     */
    public DrunkardSpaceShip() {
        super();
        random = new Random();
    }

    /**
     * Does the actions of this drunkard ship for this round.
     * This is called once per round by the SpaceWars game driver.
     *
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        shieldDown();
        if(shouldTeleport())
            teleport();
        moveDrunkard();
        bashDrunkard(game.getClosestShipTo(this));
        if (shouldShoot())
            fire(game);
        super.doAction(game);
    }

    /**
     * @param closest gets the closest ship to itself
     * if the closest ship is close, and the ship should shield then this function actives the shield of
     *                the ship
     */
    private void bashDrunkard(SpaceShip closest) {
        if(getPhysics().distanceFrom(closest.getPhysics()) <= BASHING_DISTANCE)
            if(shouldShield())
                shieldOn();
    }

    /**
     * this function handles the movement of the drunkard, first chooses a direction and then moves the
     * ship in that direction
     */
    private void moveDrunkard() {
        int choice;
        if(drunk()) { // should replace the direction of the drunkard
            choice = chooseTurn();
            lastTurnChoice = choice;
        }
        else
            choice = lastTurnChoice;
        // move for a random number between the turning min to turning max, each time with or without accl
        for(int i = 0; i < random.nextInt(TURN_MAX - TURN_MIN) + TURN_MIN; i++)
            getPhysics().move(drunk(), choice);
    }

    /**
     * @return a random boolean
     */
    private boolean drunk(){
        return random.nextBoolean();
    }

    /**
     * @return a random number between -1,0,1
     */
    private int chooseTurn(){
        return random.nextInt(TURNING_CHANCE) - 1;
    }

    /**
     * @return returns true if the random number he rolled between 0 to SHOOTING_CHANCE was 0, else false
     */
    private boolean shouldShoot(){
        return random.nextInt(SHOOTING_CHANCE) == 0;
    }

    /**
     * @return returns true if the random number he rolled between 0 to TELEPORTING_CHANCE was 0, else false
     */
    private boolean shouldTeleport() {
        return random.nextInt(TELEPORTING_CHANCE) == 0;
    }

    /**
     * @return returns true if the random number he rolled between 0 to SHIELDING_CHANCE was 0, else false
     */
    private boolean shouldShield() {
        return random.nextInt(SHIELDING_CHANCE) == 0;
    }
}
