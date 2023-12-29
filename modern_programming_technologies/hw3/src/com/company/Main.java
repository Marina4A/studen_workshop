package com.company;

import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

import javax.swing.*;
import java.awt.*;
import java.util.Vector;

import org.hibernate.*;
import org.hibernate.cfg.Configuration;

import javax.persistence.Transient;

public class Main extends JFrame {
    private SessionFactory factory;

    public static void main(String[] args) throws SQLException, IOException {
        new Main();
    }

    JList<String>  lst, lst2;
    JTextField tfId, tfParent;
    DefaultListModel<String> model, model2;

    public Main() throws SQLException, IOException {
        super( "Trees" );

        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout( new GridBagLayout() );
        // setSize(300,300);
        JLabel l;

        GridBagConstraints c = new GridBagConstraints();

        Container content = getContentPane();

        model = new DefaultListModel<>();

        JScrollPane sp;

        c.gridx = 0;
        c.gridy = 0;
        l = new JLabel( "Деревья" );
        content.add( l, c );

        lst = new JList<String>(model);

        c.gridx = 0;
        c.gridy = 1;
        c.weightx = 0.75;
        c.weighty = 1;
        c.gridwidth = 2;
        c.fill = GridBagConstraints.BOTH;

        // sp = new JScrollPane();
        // sp.add(lst);

        lst.setPreferredSize( new Dimension(200,100) );
        content.add( lst, c );

        lst.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                showItems();
            }
        });

        model2 = new DefaultListModel<>();

        c.gridx = 0;
        c.gridy = 3;
        lst2 = new JList<String>(model2);
        lst2.setPreferredSize( new Dimension(200,200) );
        content.add( lst2, c );

        c = new GridBagConstraints();

        c.gridx = 0;
        c.gridy = 2;
        l = new JLabel( "Узлы" );
        content.add( l, c );

        JButton b;

        b = new JButton("добавить" );
        b.setPreferredSize(new Dimension(100, 30));
        b.addActionListener( e -> { add(); } );

        c.gridx = 0;
        c.gridy = 4;
        content.add(b, c);

        b = new JButton("Удалить" );
        b.setPreferredSize(new Dimension(100, 30));
        b.addActionListener( e -> { del(); } );

        c.gridx = 1;
        c.gridy = 4;
        content.add(b, c);

        JTextField tf;

        c.gridx = 0;
        c.gridy = 5;

        l = new JLabel("id" );
        content.add(l, c);

        c.gridx = 1;
        c.gridy = 5;
        c.fill = GridBagConstraints.BOTH;
        tfId = new JTextField("");
        tfId.setColumns(10);
        content.add(tfId, c);

        c.gridx = 0;
        c.gridy = 6;
        l = new JLabel( "parent" );
        content.add(l, c);

        c.gridx = 1;
        c.gridy = 6;
        c.fill = GridBagConstraints.BOTH;
        tfParent = new JTextField("");
        // tfParent.setColumns(10);
        content.add( tfParent, c );

        setSize(300, 400);
        setVisible(true);

        readDb();
        showTrees();
    }

    void showTrees()
    {
        model.clear();

        if (tree == null)
            return;

        List<Node> roots = tree.getRoots();

        for( int i = 0; i < roots.size(); i++ )
            model.add( i,"" + roots.get(i).getId() );
    }

    void showItems()
    {
        int sel = lst.getSelectedIndex();

        List<Node> roots = tree.getRoots();

        List<Node> child = roots.get(sel).child;

        model2.clear();

        for( int i = 0; i < child.size(); i++ )
            model2.add( i, "" + child.get(i).getId() );
    }

    void add()
    {
        if (tree == null)
            return;

        int id, parent = 0;

        id = Integer.parseInt( tfId.getText() );
        if (tfParent.getText() != "")
            parent = Integer.parseInt( tfParent.getText() );


        tree.add( id, parent );

        showTrees();
    }

    void del()
    {
        if (tree == null)
            return;

        int id;

        id = Integer.parseInt( tfId.getText() );

        tree.del( id );

        showTrees();
    }

    Tree tree;

    void readDb() throws SQLException, IOException {
        try {
            factory = new Configuration().configure().buildSessionFactory();
        } catch (Throwable ex) {
            System.err.println("Failed to create sessionFactory object." + ex);
            throw new ExceptionInInitializerError(ex);
        }

        tree = new Tree();


        // Call it to create db
        createTable();

        Session session = factory.openSession();
        Transaction tx = null;

        List nodes = session.createQuery( "FROM Node" ).list();
        for( Iterator it = nodes.iterator(); it.hasNext(); )
        {
            Node n = (Node) it.next();
            tree.add(n);
        }

        /* List<Node> roots = tree.getRoots();

        for( int i = 0; i < roots.size(); i++ )
            System.out.println( roots.get(i).getId()); // */
    }

    static void analyze(Tree t) throws Exception {
        List<Node> roots = t.getRoots();

        int max, maxid, maxcnt, cnt;

        max = 0;
        maxid = 0;
        maxcnt = 0;

        for( int i = 0; i < roots.size(); i++ )
        {
            cnt = roots.get(i).leafCount();

            if (cnt > max)
            {
                max = cnt;
                maxid = roots.get(i).getId();
                maxcnt = 1;
            }
            else if (cnt == max)
                maxcnt++;
        }

        FileWriter wr = new FileWriter( "output.txt" );

        if (maxcnt != 1)
            wr.write( "0,0\n" );
        else
            wr.write( maxid + "," + max + "\n" );

        wr.close();
    }

    // Initialize db and fill it with data
    public void createTable() throws SQLException, IOException {
        Session sess = factory.openSession();
        Transaction tx = sess.beginTransaction();

        BufferedReader reader = new BufferedReader(new FileReader("input.csv"));

        while (true)
        {
            String line = reader.readLine();
            if (line == null)
                break;
            String[] col = line.split( "," );
            if (col.length < 2)
                break;

            Node n = new Node( Integer.parseInt(col[0]), Integer.parseInt(col[1]) );
            sess.save(n);
        }

        reader.close();

        tx.commit();
        sess.close();
    }
}
