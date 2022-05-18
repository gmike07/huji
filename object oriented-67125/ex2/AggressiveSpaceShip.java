/**
 * This class represents an aggressive space ship, which extends the class SpaceShip and overrides the
 * doAction function
 */
public class AggressiveSpaceShip extends SpaceShip{

    /* this constant holds the maximum angle to allow the space ship to shoot */
    private static final double MAXIMUM_ANGLE = 0.21;

    /**
     * Does the actions of this aggressive ship for this round.
     * This is called once per round by the SpaceWars game driver.
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game) {
        double angle = getAngleToClosest(game);
        getPhysics().move(true, angleToTurn(angle));
        if (Math.abs(angle) < MAXIMUM_ANGLE)
            fire(game);
        super.doAction(game);
    }
}
