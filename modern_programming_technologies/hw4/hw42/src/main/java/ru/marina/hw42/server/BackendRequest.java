package ru.marina.hw42.server;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;

public class BackendRequest {
    private static final String defaultScheme = "http";
    private static final String defaultHost = "localhost";
    private static final int defaultPort = 8080;
    private static final String pathPrefix = "/api/trees";

    private final String host;
    private final String scheme;
    private final int port;


    public BackendRequest() {
        this.host = defaultHost;
        this.scheme = defaultScheme;
        this.port = 8080;
    }

    public List<NodeEntity> getNodes() {
        List<NodeEntity> lst = new ArrayList<>();
        HttpURLConnection con = null;
        StringBuilder response = new StringBuilder();
        try {
            con = (HttpURLConnection)
                    new URI(scheme, null, host, port, pathPrefix, null, null).
                    toURL().openConnection();
            con.setRequestMethod("GET");
            con.setRequestProperty("Accept", "application/json");
            int responseCode = con.getResponseCode();
            if (responseCode < 200 || responseCode >= 300) {
                throw new RuntimeException("Respond code from server: " + responseCode);
            }
            try (InputStream cis = con.getInputStream();
                 InputStreamReader isr = new InputStreamReader(cis);
                 BufferedReader br = new BufferedReader(isr)) {

                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            }
        } catch (MalformedURLException | URISyntaxException e) {
            throw new RuntimeException("Invalid url syntax for nodes get request", e);
        } catch (IOException e) {
            throw new RuntimeException("Connection error", e);
        }
        finally {
            if (con != null) {
                con.disconnect();
            }
        }
        return new Gson().fromJson(response.toString(), new TypeToken<List<NodeEntity>>(){}.getType());
    }

    public NodeEntity addNode(NodeEntity n) {
        HttpURLConnection con = null;
        StringBuilder response = new StringBuilder();
        try {
            con = (HttpURLConnection)
                    new URI(scheme, null, host, port, pathPrefix, null, null).
                            toURL().openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.setDoOutput(true);
            byte[] input = new Gson().toJson(n, n.getClass()).getBytes(StandardCharsets.UTF_8);
            try(OutputStream os = con.getOutputStream()) {
                os.write(input, 0, input.length);
            }
            int responseCode = con.getResponseCode();
            if (responseCode < 200 || responseCode >= 300) {
                throw new RuntimeException("Respond code from server: " + responseCode);
            }
            try (InputStream cis = con.getInputStream();
                 InputStreamReader isr = new InputStreamReader(cis);
                 BufferedReader br = new BufferedReader(isr)) {

                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            }
        } catch (MalformedURLException | URISyntaxException e) {
            throw new RuntimeException("Invalid url syntax for get nodes request", e);
        } catch (IOException e) {
            throw new RuntimeException("Connection error", e);
        }
        finally {
            if (con != null) {
                con.disconnect();
            }
        }
        return new Gson().fromJson(response.toString(), NodeEntity.class);
    }

    public NodeEntity deleteNode(long id) {
        HttpURLConnection con = null;
        StringBuilder response = new StringBuilder();
        try {
            con = (HttpURLConnection)
                    new URI(scheme, null, host, port, pathPrefix + "/" + id, null, null).
                            toURL().openConnection();
            con.setRequestMethod("DELETE");
            con.setRequestProperty("Content-Type", "application/json");
            con.setRequestProperty("Accept", "application/json");
            con.setDoOutput(false);
            int responseCode = con.getResponseCode();
            if (responseCode < 200 || responseCode >= 300) {
                throw new RuntimeException("Respond code from server: " + responseCode);
            }
        } catch (MalformedURLException | URISyntaxException e) {
            throw new RuntimeException("Invalid url syntax for get nodes request", e);
        } catch (IOException e) {
            throw new RuntimeException("Connection error", e);
        }
        finally {
            if (con != null) {
                con.disconnect();
            }
        }
        return new Gson().fromJson(response.toString(), NodeEntity.class);
    }
}
