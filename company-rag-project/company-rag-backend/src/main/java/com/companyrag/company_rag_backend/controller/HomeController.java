package com.companyrag.company_rag_backend.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {

@GetMapping("/")
    public Map<String, String> home() {
        return Map.of(
            "application", "Company Documentation RAG AI",
            "service", "Java Spring Boot Backend",
            "status", "UP"
        );
    }

    @GetMapping("/api/health")
    public Map<String, String> health() {
        return Map.of(
            "service", "Java Backend",
            "status", "UP"
        );
    }
    
}
