/**
 * This class represents a special space ship, which extends the class SpaceShip and overrides the
 * doAction function, gotHit function
 */
public class SpecialSpaceShip extends SpaceShip{

    /* this constant holds the maximum angle to allow the space ship to shoot */
    private static final double BASHING_DISTANCE = 0.19;

    /* this constant hold the frame in which the ship should preform a shooting */
    private static final int DO_SHOOTING_COUNTER = 10;

    /* this constant hold the fire and shield rate at the break time of this ship */
    private static final int BREAK_FIRE_RATE = 10;

    /* this constant holds the max timer of the second phase, how often the ship preforms actions in the
    level */
    private static final int TELEPORT_MAX = 300;

    /* this constant holds the maximum angle to allow the space ship to shoot */
    private static final double SHOOTING_ANGLE = 0.21;

    /* this constant holds the amount of times the ship should shoot in the second phase */
    private static final int SHOOTING_AMOUNT = 360;

    /* this variable holds the timer of the second phase, when to preform a shooting and a teleport */
    private int teleportCounter = TELEPORT_MAX;


    /* this variable hold the current level of the ship, a number 1,2,3 and the ship has a different phase
    for each level*/
    private int level;

    public SpecialSpaceShip(){
        super();
        level = 1;
    }

    /**
     * This method is called whenever a ship has died. It resets the ship's
     * attributes, and starts it at a new random position, and updates the level of the ship.
     */
    @Override
    public void reset(){
        level++;
        if(level == 2 + 1)
            level = 1;
        super.reset();
    }

    /**
     * Does the actions of this special ship for this round.
     * This is called once per round by the SpaceWars game driver.
     *
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game){
        if(level == 1)
            levelOneHandler(game);
        if(level == 2)
            levelTwoHandler(game);
        super.doAction(game);
    }

    /**
     * this function handles the action of the spaceship while level = 1
     * @param game the game object to which this ship belongs.
     */
    private void levelOneHandler(SpaceWars game){
        this.shieldDown();
        SpaceShip closestShip = game.getClosestShipTo(this);
        double angle = this.getPhysics().angleTo(closestShip.getPhysics());
        this.getPhysics().move(true, angleToTurn(angle));
        if(this.getPhysics().distanceFrom(closestShip.getPhysics()) <= BASHING_DISTANCE)
            this.shieldOn();
        else if (Math.abs(angle) < SHOOTING_ANGLE)
            this.fire(game);
    }

    /**
     * fires a shot for free.
     * @param game the game object.
     */
    private void firing(SpaceWars game){
        game.addShot(this.getPhysics());
    }


    /**
     * this function handles the action of the spaceship while level = 3
     * @param game the game object to which this ship belongs.
     */
    private void levelTwoHandler(SpaceWars game){
        this.shieldDown();
        teleportCounter--;
        if(teleportCounter == DO_SHOOTING_COUNTER) {
            //kind of teleport
            for (int i = 0; i < SHOOTING_AMOUNT; i++) {
                this.getPhysics().move(false, 1);
                this.firing(game);
            }
        }
        else if(teleportCounter == 0)
            teleportCounter = TELEPORT_MAX;
        else
            breakHandler(game, teleportCounter);
    }

    /**
     * @param game the game object to which this ship belongs.
     * @param counter an integer representing a counter
     * if the counter % BREAK_FIRE_RATE is 0, then this function puts up a shield and shoots
     */
    private void breakHandler(SpaceWars game, int counter) {
        if(counter % BREAK_FIRE_RATE == 0) {
                this.fire(game);
                this.shieldUp();
        }
    }

    /**
     * This method is called by the SpaceWars game object when ever this ship
     * gets hit by a shot. in level 3, this ship DOESN'T take bullet damage.
     */
    @Override
    public void gotHit(){
        if(level != 2)
            super.gotHit();
    }

}
