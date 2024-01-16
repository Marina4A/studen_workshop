package ru.marina.ui;

import ru.marina.services.TreeService;
import ru.marina.tree.Node;
import ru.marina.tree.Tree;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.TreeModel;
import javax.swing.tree.TreeSelectionModel;
import java.awt.*;

import static javax.swing.JOptionPane.ERROR_MESSAGE;

public class Ui {
    private final JFrame mainFrame = new JFrame("Homework #2: Tree utility");

    private final JTree jTree = new JTree(new DefaultMutableTreeNode("Trees"));

    private Tree tree;

    private boolean isTreeNodeSelected = false;
    private boolean isNewNodeEmpty = true;

    public Ui(Tree tree) {
        this.tree = tree;
        buildUi();
    }

    public void launch() {
        SwingUtilities.invokeLater(() -> {
            mainFrame.pack();
            mainFrame.setVisible(true);
        });
    }

    private void buildUi() {
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainFrame.setPreferredSize(new Dimension(400, 600));
        mainFrame.setTitle("Homework #3");

        // ###### whole frame panel with borders
        JPanel mainFramePanel = new JPanel(new BorderLayout());
        mainFramePanel.setBorder(new EmptyBorder(4, 4, 4, 4));
        mainFrame.getContentPane().add(mainFramePanel);

        // ====== Upper part of main panel -- header label
        JLabel headerLabel = new JLabel("");
        mainFramePanel.add(headerLabel, BorderLayout.PAGE_START);

        // ====== lower part of main panel -- all buttons and id textedit
        JPanel buttonsPanel = new JPanel();
        buttonsPanel.setBorder(new EmptyBorder(5, 0, 0, 0));
        buttonsPanel.setLayout(new BoxLayout(buttonsPanel, BoxLayout.X_AXIS));
        mainFramePanel.add(buttonsPanel, BorderLayout.PAGE_END);

        // ------ "read" button
        JButton readTreeButton = new JButton("Read tree");
        readTreeButton.addActionListener(e -> setTree(TreeService.readFromDB()));
        buttonsPanel.add(readTreeButton);

        // ------ "add" buttons and newNodeTextEdit
        JButton addNodeButton = new JButton("Add");
        JTextField newNodeIdText = new JTextField();
        configureAddNodeButton(addNodeButton, newNodeIdText);
        configureNewNodeText(newNodeIdText, addNodeButton);

        buttonsPanel.add(addNodeButton);
        buttonsPanel.add(newNodeIdText);

        // ------ "delete" button
        JButton deleteNodeButton = makeDelNodeButton();
        buttonsPanel.add(deleteNodeButton);

        // ====== center part of main panel -- JTrees
        jTree.getSelectionModel().setSelectionMode(TreeSelectionModel.SINGLE_TREE_SELECTION);

        jTree.addTreeSelectionListener(new TreeSelectionListener() {
            @Override
            public void valueChanged(TreeSelectionEvent e) {
                DefaultMutableTreeNode node = (DefaultMutableTreeNode) jTree.getLastSelectedPathComponent();
                isTreeNodeSelected = (node != null);
                deleteNodeButton.setEnabled(isTreeNodeSelected);
                addNodeButton.setEnabled(isTreeNodeSelected && !isNewNodeEmpty);
            }
        });

        mainFramePanel.add(jTree, BorderLayout.CENTER);

    }

    private void configureNewNodeText(JTextField newNodeIdText, JButton addNodeButton) {
        newNodeIdText.getDocument().addDocumentListener(new DocumentListener() {
            private void setFlag() {
                String v = newNodeIdText.getText();
                isNewNodeEmpty = v == null || v.isEmpty();
                addNodeButton.setEnabled(isTreeNodeSelected && !isNewNodeEmpty);
            }

            @Override
            public void insertUpdate(DocumentEvent e) { setFlag();}

            @Override
            public void removeUpdate(DocumentEvent e) { setFlag(); }

            @Override
            public void changedUpdate(DocumentEvent e) { setFlag();}
        });

        Dimension dimension = newNodeIdText.getPreferredSize();
        dimension.width = 100;
        newNodeIdText.setPreferredSize(dimension);
    }

    private void configureAddNodeButton(JButton addNodeButton, JTextField newNodeIdText) {
        addNodeButton.addActionListener(event -> {
            DefaultMutableTreeNode nodeView = (DefaultMutableTreeNode) jTree.getLastSelectedPathComponent();
            if (nodeView == null) {
                return;
            }
            String s = (String) nodeView.getUserObject();
            if (s == null) {
                return;
            }
            try {
                int parentId = Integer.parseInt(s);
                Node node = tree.getNodeById(tree, parentId);
                if (node == null) {
                    return;
                }
                s = newNodeIdText.getText();
                if (s == null) {
                    return;
                }
                int id = Integer.parseInt(s);
                TreeService.addToDB(id, parentId);
                setTree(TreeService.readFromDB());
            } catch (Exception e) {
                JOptionPane.showMessageDialog(jTree,
                        e.getMessage(),
                        "Ошибка", ERROR_MESSAGE);
            }
        });
        addNodeButton.setEnabled(false);
    }

    private JButton makeDelNodeButton() {
        JButton delNodeButton = new JButton("Del");
        delNodeButton.addActionListener(event -> {
            DefaultMutableTreeNode nodeView = (DefaultMutableTreeNode) jTree.getLastSelectedPathComponent();
            if (nodeView == null) {
                return;
            }
            String s = (String) nodeView.getUserObject();
            if (s == null) {
                return;
            }
            try {
                int id = Integer.parseInt(s);
                Node node = tree.getNodeById(tree, id);
                if (node == null) {
                    return;
                }

                TreeService.deleteFromDB(tree.getNodeById(tree, id));
                setTree(TreeService.readFromDB());
            } catch (Exception e) {
                JOptionPane.showMessageDialog(jTree,
                        e.getMessage(),
                        "Ошибка", ERROR_MESSAGE);
                return;
            }
        });
        delNodeButton.setEnabled(false);
        return delNodeButton;
    }

    private void populateTreeRecursive(Node node, DefaultMutableTreeNode nodeView) {
        for (Node n: node.getChildren()) {
            DefaultMutableTreeNode newNodeView = new DefaultMutableTreeNode(n.toString());
            nodeView.add(newNodeView);
            populateTreeRecursive(n, newNodeView);
        }

    }
    private void populateTree() {
        TreeModel treeModel = jTree.getModel();
        DefaultMutableTreeNode rootView = (DefaultMutableTreeNode) treeModel.getRoot();
        rootView.removeAllChildren();
        populateTreeRecursive(tree.getRoot(), rootView);
        jTree.updateUI();
    }

    public void setTree(Tree tree) {
        this.tree = tree;
        populateTree();
        for (int i = 0; i < jTree.getRowCount(); i++) {
            jTree.expandRow(i);
        }
    }
}
