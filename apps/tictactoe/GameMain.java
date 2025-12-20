package tictactoe;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class GameMain {

	public static void main(String args[]) {
		EventQueue.invokeLater(new Runnable(){
			   public void run()
			   {
			    TicTacToeFrame frame=new TicTacToeFrame();
			   }
			  });
	}
}
