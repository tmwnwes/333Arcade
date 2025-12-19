package chopstick;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class ChopsticksGame extends JFrame {
    private static final int MAX_FINGERS = 5;
    
    // Game state
    private int[] player1Hand = {1, 1};
    private int[] player2Hand = {1, 1};
    private int currentPlayer = 1;
    private boolean gameOver = false;
    private GameMode currentMode = GameMode.NONE;
    
    // UI Components
    private JLabel statusLabel;
    private JLabel turnLabel;
    private JPanel player1Panel, player2Panel;
    private JButton[][] player1Buttons, player2Buttons;
    private JButton[] actionButtons;
    private JTextArea gameLog;
    private JButton newGameButton;
    
    private enum GameMode {
        NONE, ATTACK, SPLIT
    }
    
    public ChopsticksGame() {
        setTitle("Chopsticks Game");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());
        getContentPane().setBackground(new Color(240, 240, 220));
        
        initializeGame();
        setupUI();
        
        pack();
        setSize(900, 700);
        setLocationRelativeTo(null);
        setVisible(true);
    }
    
    private void initializeGame() {
        player1Hand = new int[]{1, 1};
        player2Hand = new int[]{1, 1};
        currentPlayer = 1;
        gameOver = false;
        currentMode = GameMode.NONE;
    }
    
    private void setupUI() {
        // North Panel - Game Status
        JPanel topPanel = new JPanel(new BorderLayout());
        topPanel.setBackground(new Color(180, 200, 180));
        
        statusLabel = new JLabel("Chopsticks Game - Player 1's Turn", SwingConstants.CENTER);
        statusLabel.setFont(new Font("Arial", Font.BOLD, 20));
        statusLabel.setForeground(new Color(50, 70, 50));
        
        turnLabel = new JLabel("Make your move!", SwingConstants.CENTER);
        turnLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        
        topPanel.add(statusLabel, BorderLayout.NORTH);
        topPanel.add(turnLabel, BorderLayout.CENTER);
        
        add(topPanel, BorderLayout.NORTH);
        
        // Center Panel - Game Board
        JPanel centerPanel = new JPanel(new GridLayout(1, 2, 20, 0));
        centerPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        centerPanel.setBackground(new Color(240, 240, 220));
        
        // Player 1 Panel
        player1Panel = createPlayerPanel("Player 1", Color.BLUE, true);
        player1Buttons = createHandButtons(player1Panel, 1);
        
        // Player 2 Panel
        player2Panel = createPlayerPanel("Player 2", Color.RED, false);
        player2Buttons = createHandButtons(player2Panel, 2);
        
        centerPanel.add(player1Panel);
        centerPanel.add(player2Panel);
        
        add(centerPanel, BorderLayout.CENTER);
        
        // South Panel - Controls
        JPanel southPanel = new JPanel(new BorderLayout());
        southPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 20, 20));
        
        // Action Buttons
        JPanel actionPanel = new JPanel(new GridLayout(1, 4, 10, 0));
        actionButtons = new JButton[4];
        String[] actionLabels = {"Attack", "Split", "Pass", "Rules"};
        
        for (int i = 0; i < actionButtons.length; i++) {
            actionButtons[i] = new JButton(actionLabels[i]);
            actionButtons[i].setFont(new Font("Arial", Font.BOLD, 14));
            actionButtons[i].setBackground(new Color(200, 220, 200));
            actionPanel.add(actionButtons[i]);
        }
        
        // Game Log
        gameLog = new JTextArea(8, 50);
        gameLog.setEditable(false);
        gameLog.setFont(new Font("Monospaced", Font.PLAIN, 12));
        gameLog.setBackground(new Color(250, 250, 240));
        JScrollPane scrollPane = new JScrollPane(gameLog);
        
        // New Game Button
        newGameButton = new JButton("New Game");
        newGameButton.setFont(new Font("Arial", Font.BOLD, 14));
        newGameButton.setBackground(new Color(180, 200, 220));
        
        JPanel bottomPanel = new JPanel(new BorderLayout());
        bottomPanel.add(actionPanel, BorderLayout.NORTH);
        bottomPanel.add(scrollPane, BorderLayout.CENTER);
        bottomPanel.add(newGameButton, BorderLayout.SOUTH);
        
        southPanel.add(bottomPanel, BorderLayout.CENTER);
        add(southPanel, BorderLayout.SOUTH);
        
        // Setup Action Listeners
        setupActionListeners();
        
        updateUI();
    }
    
    private JPanel createPlayerPanel(String playerName, Color color, boolean isLeftPlayer) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createLineBorder(color, 3, true));
        panel.setBackground(new Color(255, 255, 240));
        
        JLabel nameLabel = new JLabel(playerName, SwingConstants.CENTER);
        nameLabel.setFont(new Font("Arial", Font.BOLD, 18));
        nameLabel.setForeground(color);
        panel.add(nameLabel, BorderLayout.NORTH);
        
        JPanel handPanel = new JPanel(new GridLayout(2, 1, 10, 10));
        handPanel.setBackground(new Color(255, 255, 240));
        panel.add(handPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JButton[][] createHandButtons(JPanel playerPanel, int playerNumber) {
        JButton[][] buttons = new JButton[2][1];
        JPanel handPanel = (JPanel) playerPanel.getComponent(1);
        
        String[] handNames = {"Left Hand", "Right Hand"};
        
        for (int i = 0; i < 2; i++) {
            JPanel singleHandPanel = new JPanel(new BorderLayout());
            singleHandPanel.setBorder(BorderFactory.createTitledBorder(handNames[i]));
            
            buttons[i][0] = new JButton("1");
            buttons[i][0].setFont(new Font("Arial", Font.BOLD, 24));
            buttons[i][0].setPreferredSize(new Dimension(80, 80));
            buttons[i][0].setEnabled(false);
            
            singleHandPanel.add(buttons[i][0], BorderLayout.CENTER);
            handPanel.add(singleHandPanel);
        }
        
        return buttons;
    }
    
    private void setupActionListeners() {
        // Attack Button
        actionButtons[0].addActionListener(e -> {
            if (!gameOver && currentMode == GameMode.NONE) {
                enterAttackMode();
            }
        });
        
        // Split Button
        actionButtons[1].addActionListener(e -> {
            if (!gameOver && currentMode == GameMode.NONE) {
                enterSplitMode();
            }
        });
        
        // Pass Button
        actionButtons[2].addActionListener(e -> {
            if (!gameOver && currentMode == GameMode.NONE) {
                addToGameLog("Player " + currentPlayer + " passed their turn.");
                switchTurn();
                updateUI();
            }
        });
        
        // Rules Button
        actionButtons[3].addActionListener(e -> showRules());
        
        // New Game Button
        newGameButton.addActionListener(e -> {
            initializeGame();
            updateUI();
            addToGameLog("=== New Game Started ===");
        });
    }
    
    private void enterAttackMode() {
        currentMode = GameMode.ATTACK;
        turnLabel.setText("Select YOUR hand to attack with");
        enableCurrentPlayerHands(true);
        disableActionButtons();
    }
    
    private void enterSplitMode() {
        currentMode = GameMode.SPLIT;
        turnLabel.setText("Select the hand you want to SPLIT FROM");
        enableCurrentPlayerHands(true);
        disableActionButtons();
    }
    
    private void enableCurrentPlayerHands(boolean enable) {
        JButton[][] buttons = (currentPlayer == 1) ? player1Buttons : player2Buttons;
        int[] hand = (currentPlayer == 1) ? player1Hand : player2Hand;
        
        for (int i = 0; i < 2; i++) {
            if (hand[i] > 0) {
                buttons[i][0].setEnabled(enable);
                if (enable) {
                    // Remove existing listeners first
                    for (ActionListener al : buttons[i][0].getActionListeners()) {
                        buttons[i][0].removeActionListener(al);
                    }
                    buttons[i][0].addActionListener(new HandSelectionHandler(i));
                }
            }
        }
    }
    
    private void disableActionButtons() {
        for (int i = 0; i < 3; i++) {
            actionButtons[i].setEnabled(false);
        }
    }
    
    private void enableActionButtons() {
        for (int i = 0; i < 3; i++) {
            actionButtons[i].setEnabled(true);
        }
    }
    
    private class HandSelectionHandler implements ActionListener {
        private int selectedHandIndex;
        
        public HandSelectionHandler(int handIndex) {
            this.selectedHandIndex = handIndex;
        }
        
        @Override
        public void actionPerformed(ActionEvent e) {
            if (currentMode == GameMode.ATTACK) {
                handleAttackSelection(selectedHandIndex);
            } else if (currentMode == GameMode.SPLIT) {
                handleSplitSelection(selectedHandIndex);
            }
        }
    }
    
    private int firstSelectedHand = -1;
    
    private void handleAttackSelection(int handIndex) {
        if (firstSelectedHand == -1) {
            // First selection: attacker's hand
            firstSelectedHand = handIndex;
            turnLabel.setText("Now select OPPONENT's hand to attack");
            
            // Disable current player's hands, enable opponent's hands
            enableCurrentPlayerHands(false);
            enableOpponentHands(true);
        } else {
            // Second selection: target hand
            performAttack(firstSelectedHand, handIndex);
            resetSelection();
        }
    }
    
    private void handleSplitSelection(int handIndex) {
        if (firstSelectedHand == -1) {
            // First selection: source hand
            int[] currentPlayerHand = (currentPlayer == 1) ? player1Hand : player2Hand;
            
            if (currentPlayerHand[handIndex] == 0) {
                JOptionPane.showMessageDialog(this, "Cannot split from a dead hand!");
                return;
            }
            
            firstSelectedHand = handIndex;
            turnLabel.setText("Now select YOUR other hand to split to");
            
            // Enable current player's hands except the selected one
            JButton[][] buttons = (currentPlayer == 1) ? player1Buttons : player2Buttons;
            for (int i = 0; i < 2; i++) {
                if (i == handIndex) {
                    buttons[i][0].setEnabled(false);
                } else {
                    buttons[i][0].setEnabled(true);
                    // Remove existing listeners and add new ones
                    for (ActionListener al : buttons[i][0].getActionListeners()) {
                        buttons[i][0].removeActionListener(al);
                    }
                    buttons[i][0].addActionListener(new HandSelectionHandler(i));
                }
            }
        } else {
            // Second selection: destination hand
            if (firstSelectedHand == handIndex) {
                JOptionPane.showMessageDialog(this, "Cannot split to the same hand!");
                resetSelection();
                enterSplitMode();
                return;
            }
            
            performSplit(firstSelectedHand, handIndex);
            resetSelection();
        }
    }
    
    private void enableOpponentHands(boolean enable) {
        int opponent = (currentPlayer == 1) ? 2 : 1;
        JButton[][] buttons = (opponent == 1) ? player1Buttons : player2Buttons;
        int[] hand = (opponent == 1) ? player1Hand : player2Hand;
        
        for (int i = 0; i < 2; i++) {
            if (hand[i] > 0) {
                buttons[i][0].setEnabled(enable);
                if (enable) {
                    // Remove existing listeners first
                    for (ActionListener al : buttons[i][0].getActionListeners()) {
                        buttons[i][0].removeActionListener(al);
                    }
                    buttons[i][0].addActionListener(new HandSelectionHandler(i));
                }
            }
        }
    }
    
    private void resetSelection() {
        firstSelectedHand = -1;
        currentMode = GameMode.NONE;
        disableAllHands();
        enableActionButtons();
    }
    
    private void disableAllHands() {
        for (int i = 0; i < 2; i++) {
            player1Buttons[i][0].setEnabled(false);
            player2Buttons[i][0].setEnabled(false);
            
            // Remove all action listeners
            for (ActionListener al : player1Buttons[i][0].getActionListeners()) {
                player1Buttons[i][0].removeActionListener(al);
            }
            for (ActionListener al : player2Buttons[i][0].getActionListeners()) {
                player2Buttons[i][0].removeActionListener(al);
            }
        }
    }
    
    private void performAttack(int attackerHand, int targetHand) {
        int[] attacker = (currentPlayer == 1) ? player1Hand : player2Hand;
        int[] target = (currentPlayer == 1) ? player2Hand : player1Hand;
        
        int attackValue = attacker[attackerHand];
        
        if (attackValue == 0) {
            JOptionPane.showMessageDialog(this, "Cannot attack with a dead hand!");
            return;
        }
        
        target[targetHand] += attackValue;
        
        if (target[targetHand] >= MAX_FINGERS) {
            target[targetHand] = 0;
        }
        
        addToGameLog("Player " + currentPlayer + " attacked with " + 
                    (attackerHand == 0 ? "Left" : "Right") + " hand (" + attackValue + 
                    ") -> Opponent's " + (targetHand == 0 ? "Left" : "Right") + " hand");
        
        checkGameOver();
        if (!gameOver) {
            switchTurn();
        }
        updateUI();
    }
    
    private void performSplit(int fromHand, int toHand) {
        int[] player = (currentPlayer == 1) ? player1Hand : player2Hand;
        
        if (fromHand == toHand) {
            JOptionPane.showMessageDialog(this, "Cannot split to the same hand!");
            return;
        }
        
        if (player[fromHand] == 0) {
            JOptionPane.showMessageDialog(this, "Cannot split from a dead hand!");
            return;
        }
        
        if (player[toHand] == 0) {
            JOptionPane.showMessageDialog(this, "Cannot split to a dead hand!");
            return;
        }
        
        // Calculate total fingers
        int total = player[fromHand] + player[toHand];
        
        // Check if split is valid
        if (total % 2 != 0) {
            JOptionPane.showMessageDialog(this, "Invalid split! Total must be even.");
            return;
        }
        
        int newValue = total / 2;
        
        // Check if new value would be 5 or more
        if (newValue >= MAX_FINGERS) {
            JOptionPane.showMessageDialog(this, "Invalid split! Resulting hands would have " + newValue + 
                                          " fingers (maximum is " + (MAX_FINGERS - 1) + ")");
            return;
        }
        
        // Perform the split
        player[fromHand] = newValue;
        player[toHand] = newValue;
        
        addToGameLog("Player " + currentPlayer + " split: " + 
                    (fromHand == 0 ? "Left" : "Right") + " and " + 
                    (toHand == 0 ? "Left" : "Right") + " hands now both have " + newValue + " fingers");
        
        switchTurn();
        updateUI();
    }
    
    private void switchTurn() {
        currentPlayer = (currentPlayer == 1) ? 2 : 1;
    }
    
    private void checkGameOver() {
        boolean player1Dead = (player1Hand[0] == 0 && player1Hand[1] == 0);
        boolean player2Dead = (player2Hand[0] == 0 && player2Hand[1] == 0);
        
        if (player1Dead || player2Dead) {
            gameOver = true;
            String winner = player1Dead ? "Player 2" : "Player 1";
            statusLabel.setText("Game Over! " + winner + " Wins!");
            turnLabel.setText("Click 'New Game' to play again");
            
            addToGameLog("=== GAME OVER ===");
            addToGameLog(winner + " wins the game!");
        }
    }
    
    private void updateUI() {
        // Update player 1 hand displays
        for (int i = 0; i < 2; i++) {
            player1Buttons[i][0].setText(String.valueOf(player1Hand[i]));
            updateButtonColor(player1Buttons[i][0], player1Hand[i]);
        }
        
        // Update player 2 hand displays
        for (int i = 0; i < 2; i++) {
            player2Buttons[i][0].setText(String.valueOf(player2Hand[i]));
            updateButtonColor(player2Buttons[i][0], player2Hand[i]);
        }
        
        // Update status
        if (!gameOver) {
            statusLabel.setText("Chopsticks Game - Player " + currentPlayer + "'s Turn");
            statusLabel.setForeground(currentPlayer == 1 ? Color.BLUE : Color.RED);
            if (currentMode == GameMode.NONE) {
                turnLabel.setText("Select an action: Attack or Split");
            }
        }
        
        // Update borders to show current player
        player1Panel.setBorder(BorderFactory.createLineBorder(
            currentPlayer == 1 ? Color.BLUE : Color.GRAY, 
            currentPlayer == 1 ? 4 : 2, 
            true));
        player2Panel.setBorder(BorderFactory.createLineBorder(
            currentPlayer == 2 ? Color.RED : Color.GRAY, 
            currentPlayer == 2 ? 4 : 2, 
            true));
    }
    
    private void updateButtonColor(JButton button, int value) {
        if (value == 0) {
            button.setBackground(Color.DARK_GRAY);
            button.setForeground(Color.WHITE);
        } else if (value >= 4) {
            button.setBackground(Color.RED);
            button.setForeground(Color.WHITE);
        } else if (value >= 2) {
            button.setBackground(Color.ORANGE);
            button.setForeground(Color.BLACK);
        } else {
            button.setBackground(Color.GREEN);
            button.setForeground(Color.BLACK);
        }
    }
    
    private void addToGameLog(String message) {
        String timestamp = new java.text.SimpleDateFormat("HH:mm:ss").format(new Date());
        gameLog.append("[" + timestamp + "] " + message + "\n");
        gameLog.setCaretPosition(gameLog.getDocument().getLength());
    }
    
    private void showRules() {
        String rules = """
            CHOPSTICKS GAME RULES:
            
            1. Each player starts with 1 finger on each hand (left and right).
            
            2. On your turn, you can either:
               - ATTACK: Tap one of your hands against an opponent's hand.
                 The opponent adds your fingers to theirs.
                 If a hand reaches 5 or more fingers, it becomes "dead" (returns to 0).
               
               - SPLIT: Redistribute your fingers between your own hands.
                 The total fingers must be even.
                 Both hands end up with the same number after split.
                 You cannot split if one hand is dead (0).
                 
               - PASS: Skip your turn.
            
            3. You cannot split to create a hand with 5 or more fingers.
            
            4. You win when both of your opponent's hands are "dead" (0 fingers).
            
            5. A hand with 0 fingers cannot be used to attack or be split from/to.
            
            SPLIT EXAMPLES:
            - (1, 3) -> (2, 2)  [Total 4, split to 2 each]
            - (0, 2) -> Cannot split (dead hand)
            - (3, 3) -> (3, 3)  [No change]
            - (4, 0) -> Cannot split (dead hand)
            """;
        
        JOptionPane.showMessageDialog(this, rules, "Game Rules", JOptionPane.INFORMATION_MESSAGE);
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
            } catch (Exception e) {
                e.printStackTrace();
            }
            new ChopsticksGame();
        });
    }
}