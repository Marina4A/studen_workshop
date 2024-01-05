package ru.marina.hw41.controllers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.marina.hw41.db.entities.NodeEntity;
import ru.marina.hw41.db.repositories.NodeRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping(produces = MediaType.APPLICATION_JSON_VALUE)
public class ForestController {
    private static final Logger log = LoggerFactory.getLogger(ForestController.class);

    @Autowired
    NodeRepository repository;

    @GetMapping(value = "/api/trees")
    public List<NodeEntity> trees() {
        List<NodeEntity> lst = new ArrayList<>();
        repository.findAll().forEach(lst::add);
        return lst;
    }

    @GetMapping(value = "/api/trees/{id}")
    public NodeEntity getNode(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Node not found. id = " + id));
    }

    @PostMapping("/api/trees")
    NodeEntity newNode(@RequestBody NodeEntity newNode) {
        return repository.save(newNode);
    }

    @PutMapping("/api/trees/{id}")
    NodeEntity replaceNode(@RequestBody NodeEntity newNode, @PathVariable Long id) {

        return repository.findById(id)
                .map(employee -> {
                    employee.setParentId(newNode.getParentId());
                    return repository.save(employee);
                })
                .orElseGet(() -> {
                    newNode.setId(id);
                    return repository.save(newNode);
                });
    }

    @DeleteMapping("/api/trees/{id}")
    ResponseEntity<NodeEntity> deleteNode(@PathVariable Long id) {
        repository.deleteById(id);
        return new ResponseEntity<>(HttpStatus.OK);
    }

}
