/**
 * This class represents a runner space ship, which extends the class SpaceShip and overrides the
 * doAction function
 */
public class RunnerSpaceShip extends SpaceShip{

    /* this constant holds the maximum distance to allow the space ship to teleport */
    private static final double RUNNING_MAXIMUM_DISTANCE = 0.25;

    /* this constant holds the maximum angle to allow the space ship to teleport */
    private static final double RUNNING_MAXIMUM_ANGLE = 0.23;

    /**
     * Does the actions of this runner ship for this round.
     * This is called once per round by the SpaceWars game driver.
     *
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        double angle = getAngleToClosest(game);
        if(getPhysics().distanceFrom(getClosestShip(game).getPhysics()) <= RUNNING_MAXIMUM_DISTANCE
                && Math.abs(angle)  < RUNNING_MAXIMUM_ANGLE)
            teleport();
        getPhysics().move(true, angleToTurn(-angle));
        super.doAction(game);
    }

    /**
     * @param angle gets an angle (double)
     * @return the number to turn 1 if turn > 0, else -1
     */
    @Override
    protected int angleToTurn(double angle){
        return angle > 0 ? 1 : -1;
    }
}