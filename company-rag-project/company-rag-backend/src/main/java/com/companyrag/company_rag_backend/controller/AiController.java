package com.companyrag.company_rag_backend.controller;

import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.companyrag.company_rag_backend.service.PythonAiService;

@RestController
@RequestMapping("/api/ai")
public class AiController {
    
     private final PythonAiService pythonAiService;

    public AiController(PythonAiService pythonAiService) {
        this.pythonAiService = pythonAiService;
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of(
                "service", "Java AI Gateway",
                "status", "UP"
        );
    }

    @GetMapping("/search")
    public Map search(
            @RequestParam String question,
            @RequestParam(defaultValue = "5") int topK) {

        return pythonAiService.searchDocuments(question, topK);
    }
    
}
