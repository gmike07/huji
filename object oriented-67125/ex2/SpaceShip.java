import java.awt.Image;
import oop.ex2.*;


/**
 * This class represents a space ship with all the function that were required.
 *
 * The API spaceships need to implement for the SpaceWars game. 
 * It is your decision whether SpaceShip.java will be an interface, an abstract class,
 *  a base class for the other spaceships or any other option you will choose.
 *
 * @author oop
 */
public class SpaceShip{

    /* this constant holds the amount of energy increased each time it should be increased */
    private static final int ENERGY_INCREASE = 18;

    /* this constant holds the amount of energy decreased each time it should be decreased */
    private static final int ENERGY_DECREASE = 10;

    /* this constant holds the duration of the shooting delay */
    private static final int MAX_SHOOTING_DELAY = 7;

    /* this constant holds the initial max health of the ship */
    private static final int MAX_HEALTH = 22;

    /* this constant holds the initial max energy of the ship */
    private static final int INITIAL_MAX_ENERGY = 210;

    /* this constant holds the initial energy of the ship */
    private static final int INITIAL_ENERGY = 190;

    /* this constant holds the cost of shooting */
    private static final int SHOOTING_COST = 19;

    /* this constant holds the cost of using a teleport */
    private static final int TELEPORTATION_COST = 140;

    /* this constant holds the cost of using a shield */
    private static final int SHIELD_COST = 3;


    /* this variable holds the physics object of the class (position) */
    private SpaceShipPhysics physics;

    /* this variable holds the current max energy of the ship */
    private int maxEnergy;

    /* this variable holds the current energy of the ship */
    private int energy;

    /* this variable holds the current health of the ship */
    private int health;

    /* this variable holds the current state of the shield of the shield, up = true, down = false */
    private boolean isShieldUp;

    /* this variable holds the cuurent delay up to the next time the ship can shoot */
    private int shootingDelay;


    /**
     * This constructor builds a new space ship as requested by the exercise
     */
    public SpaceShip() {
        reset();
    }

    /**
     * Does the actions of this ship for this round.
     * This is called once per round by the SpaceWars game driver.
     *
     * @param game the game object to which this ship belongs.
     */
    public void doAction(SpaceWars game) {
        shootingDelay = Math.max(0, shootingDelay - 1);
        energy = Math.min(maxEnergy, energy + 1);
    }

    /**
     * This method is called every time a collision with this ship occurs
     */
    public void collidedWithAnotherShip(){
        if(isShieldUp){
            maxEnergy += ENERGY_INCREASE;
            energy += ENERGY_INCREASE;
        }
        else
            handleDamage();
    }

    /**
     * This method is called whenever a ship has died. It resets the ship's
     * attributes, and starts it at a new random position.
     */
    public void reset(){
        physics = new SpaceShipPhysics();
        isShieldUp = false;
        shootingDelay = 0;
        health = MAX_HEALTH;
        maxEnergy = INITIAL_MAX_ENERGY;
        energy = INITIAL_ENERGY;
    }

    /**
     * Checks if this ship is dead.
     * @return true if the ship is dead. false otherwise.
     */
    public boolean isDead() {
        return health == 0;
    }

    /**
     * Gets the physics object that controls this ship.
     *
     * @return the physics object that controls the ship.
     */
    public SpaceShipPhysics getPhysics() {
        return physics;
    }

    /**
     * This method is called by the SpaceWars game object when ever this ship
     * gets hit by a shot.
     */
    public void gotHit() {
        if(!isShieldUp)
            handleDamage();
    }

    /**
     * this function handles the damage done to the ship
     */
    private void handleDamage() {
        health = Math.max(0, health - 1);
        maxEnergy = Math.max(maxEnergy - ENERGY_DECREASE, 0);
        energy = Math.min(energy, maxEnergy);
    }

    /**
     * Gets the image of this ship. This method should return the image of the
     * ship with or without the shield. This will be displayed on the GUI at
     * the end of the round.
     *
     * @return the image of this ship.
     */
    public Image getImage(){
        if(isShieldUp)
            return GameGUI.ENEMY_SPACESHIP_IMAGE_SHIELD;
        return GameGUI.ENEMY_SPACESHIP_IMAGE;
    }

    /**
     * Attempts to fire a shot.
     * @param game the game object.
     */
    public void fire(SpaceWars game) {
        if(shootingDelay != 0 || energy < SHOOTING_COST)
            return;
        energy = energy - SHOOTING_COST;
        shootingDelay = MAX_SHOOTING_DELAY;
        game.addShot(physics);
    }

    /**
     * Attempts to turn on the shield.
     */
    public void shieldOn() {
        if(energy < SHIELD_COST)
            return;
        energy = energy - SHIELD_COST;
        isShieldUp = true;
    }

    /**
     * Attempts to teleport.
     */
    public void teleport() {
        if(energy < TELEPORTATION_COST)
            return;
        energy = energy - TELEPORTATION_COST;
        physics = new SpaceShipPhysics();
    }

    /**
     * @param turn gets an angle (double)
     * @return the number to turn 1 if turn > 0, 0 if turn = 0, -1 if turn < 0
     */
    protected int angleToTurn(double turn){
        return (int)Math.signum(turn);
    }

    /**
     * this function lowers the shield (puts down) of this spaceship
     */
    protected void shieldDown(){
        isShieldUp = false;
    }

    /**
     * this function takes up the shield (puts up) of this spaceship
     */
    protected void shieldUp(){
        isShieldUp = true;
    }

    /**
     * @return the state of the shield (up or down - up is true)
     */
    protected boolean getShield(){
        return isShieldUp;
    }

    /**
     *  returns the closest ship to this one
     *  @param game the game object to which this ship belongs.
     */
    protected SpaceShip getClosestShip(SpaceWars game){
        return game.getClosestShipTo(this);
    }

    /**
     *  returns the angle to the closest ship to this one
     *  @param game the game object to which this ship belongs.
     */
    protected double getAngleToClosest(SpaceWars game){
        return getPhysics().angleTo(game.getClosestShipTo(this).getPhysics());
    }
}
