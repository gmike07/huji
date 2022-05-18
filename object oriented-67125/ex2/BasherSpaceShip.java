/**
 * This class represents a basher space ship, which extends the class SpaceShip and overrides the
 * doAction function
 */
public class BasherSpaceShip extends SpaceShip{

    /* this constant holds the minimum distance to allow the space ship to bash */
    private static final double BASHING_MAXIMUM_DISTANCE = 0.19;

    /**
     * Does the actions of this basher ship for this round.
     * This is called once per round by the SpaceWars game driver.
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        shieldDown();
        getPhysics().move(true, angleToTurn(getAngleToClosest(game)));
        if(getPhysics().distanceFrom(getClosestShip(game).getPhysics()) <= BASHING_MAXIMUM_DISTANCE)
            shieldOn();
        super.doAction(game);
    }
}

