import oop.ex2.GameGUI;
import java.awt.Image;
/**
 * This class represents a human space ship, which extends the class SpaceShip and overrides the
 * doAction function and getImage function
 */
public class HumanSpaceShip extends SpaceShip{

    /**
     * Does the actions of this human ship for this round.
     * This is called once per round by the SpaceWars game driver.
     *
     * @param game the game object to which this ship belongs.
     */
    @Override
    public void doAction(SpaceWars game) {
        shieldDown();
        GameGUI gui = game.getGUI();
        if(gui.isTeleportPressed())
            teleport();
        moveHuman(gui, gui.isUpPressed());
        if(gui.isShieldsPressed())
            shieldOn();
        if(gui.isShotPressed())
            fire(game);
        super.doAction(game);
    }

    /**
     * @param gui the gui of this game of class GameGUI
     * @param accl boolean should the ship accelerate
     * this function moves the ship in the correct direction and with\out acceleration
     */
    private void moveHuman(GameGUI gui, boolean accl){
        int turn = 0;
        if(gui.isLeftPressed())
            turn++;
        if(gui.isRightPressed())
            turn--;
        getPhysics().move(accl, turn);
    }

    /**
     * Gets the image of this ship. This method should return the image of the
     * ship with or without the shield. This will be displayed on the GUI at
     * the end of the round.
     *
     * @return the image of this ship.
     */
    @Override
    public Image getImage(){
        if(getShield())
            return GameGUI.SPACESHIP_IMAGE_SHIELD;
        return GameGUI.SPACESHIP_IMAGE;
    }
}
