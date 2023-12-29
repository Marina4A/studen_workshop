package com.company;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Tree {
    List<Node> roots = new ArrayList<>();
    HashMap<Integer, Node> nodes = new HashMap<Integer, Node>();

    void rec(List<Node> lst, Node n)
    {
        lst.add(n);

        for( int i = 0; i < n.getChild().size(); i++ )
            rec( lst, n.getChild().get(i) );
    }

    public List<Node> getAll()
    {
        List<Node> lst = new ArrayList<>();

        for( int i = 0; i < roots.size(); i++ )
            rec( lst, roots.get(i) );

        return lst;
    }

    public List<Node> getLeaves()
    {
        List<Node> res = new ArrayList<>(), lst;

        lst = getAll();
        for( int i = 0; i < lst.size(); i++ )
            if (lst.get(i).isLeaf())
                res.add(lst.get(i));

        return res;
    }

    public List<Node> getRoots()
    {
        return roots;
    }

    public Node add( int id, int parent_id ) {
        Node n = new Node(id, parent_id);
        add(n);

        return n;
    }

    public Node add( Node n )
    {
        if ((n.getId() != n.getParent_id()) & (n.getParent_id() != 0))
        {
            if (nodes.containsKey(n.getParent_id())) {
                Node p = nodes.get(n.getParent_id());
                p.getChild().add(n);
            }
            else
                System.out.println( "Node " + n.getParent_id() + " not found" );
        }
        else
            roots.add( n );

        nodes.put( n.getId(), n );
        return n;
    }

    public void del( int id )
    {
        if (nodes.get(id) != null)
            nodes.remove(id);
    }

    public static Tree readCsv( String fname ) throws IOException {
        Tree r = new Tree();

        BufferedReader reader = new BufferedReader(new FileReader(fname));

        while (true)
        {
            String line = reader.readLine();
            if (line == null)
                break;
            String[] col = line.split( "," );
            if (col.length < 2)
                break;

            Node n = r.add( Integer.parseInt(col[0]), Integer.parseInt(col[1]) );
            r.nodes.put( n.getId(), n );
        }

        reader.close();

        return r;
    }
}
